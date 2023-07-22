
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Constants
S0 = 100  # current stock price
r = 0.05  # annual risk-free interest rate
sigma = 0.20  # annual volatility of the stock
T = 1  # one calendar year
mu = r  # drift rate equal to risk-free rate
delta_t = 1/252  # size of a time step
num_paths = 1000  # number of simulated stock price paths
num_steps = int(T/delta_t)  # number of steps

# Initialize the array to store the paths
paths = np.zeros((num_steps + 1, num_paths))
paths[0] = S0

# Simulate the paths
np.random.seed(42)  # for reproducibility
for t in range(1, num_steps + 1):
    brownian = np.random.standard_normal(num_paths)
    paths[t] = paths[t - 1] * np.exp((mu - 0.5 * sigma**2) * delta_t + sigma * np.sqrt(delta_t) * brownian)

# Plot the first 10 simulated stock price paths
plt.figure(figsize=(10, 6))
for i in range(10):
    plt.plot(paths[:, i])
plt.title('First 10 Simulated Stock Price Paths')
plt.xlabel('Time Steps')
plt.ylabel('Stock Price')
plt.show()

# save the plot as a png file
plt.savefig('first_10_simulated_stock_price_paths.png')

# Compute the expected payoff for a call option
ST = paths[-1]
X = S0
payoff = np.maximum(ST - X, 0)
expected_payoff = np.exp(-r*T) * np.mean(payoff)
print('The expected payoff for a call option is', expected_payoff)

# Compute the Black-Scholes price for a call option
q = 0  # continuous dividend yield
d1 = (np.log(S0 / X) + (r - q + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
d2 = d1 - sigma * np.sqrt(T)
bs_price = S0 * np.exp(-q*T) * norm.cdf(d1) - X * np.exp(-r*T) * norm.cdf(d2)
print('The Black-Scholes price for a call option is', bs_price)

# Simulate the paths using the exact solution for GBM
exact_paths = np.zeros((num_steps + 1, num_paths))
exact_paths[0] = S0
for t in range(1, num_steps + 1):
    brownian = np.random.standard_normal(num_paths)
    exact_paths[t] = S0 * np.exp((r - 0.5 * sigma**2) * t*delta_t + sigma * np.sqrt(t*delta_t) * brownian)

#plot the first 10 exact paths
plt.figure(figsize=(10, 6))
for i in range(10):
    plt.plot(exact_paths[:, i])
plt.title('First 10 Exact Stock Price Paths')
plt.xlabel('Time Steps')
plt.ylabel('Stock Price')
plt.show()

# save the plot as a png file
plt.savefig('first_10_exact_stock_price_paths.png')

# Compute the expected payoff for a call option using the exact paths
exact_ST = exact_paths[-1]
exact_payoff = np.maximum(exact_ST - X, 0)
exact_expected_payoff = np.exp(-r*T) * np.mean(exact_payoff)
print('The expected payoff for a call option using the exact paths is', exact_expected_payoff)

# Compute the expected payoff for an Asian call option using the discretized GBM paths
average_ST_discretized = np.mean(paths, axis=0)
asian_payoff_discretized = np.maximum(average_ST_discretized - X, 0)
asian_expected_payoff_discretized = np.exp(-r*T) * np.mean(asian_payoff_discretized)
print('The expected payoff for an Asian call option using the discretized GBM paths is', asian_expected_payoff_discretized)

# Compute the expected payoff for an Asian call option using the exact GBM paths
average_ST_exact = np.mean(exact_paths, axis=0)
asian_payoff_exact = np.maximum(average_ST_exact - X, 0)
asian_expected_payoff_exact = np.exp(-r*T) * np.mean(asian_payoff_exact)
print('The expected payoff for an Asian call option using the exact GBM paths is', asian_expected_payoff_exact)
