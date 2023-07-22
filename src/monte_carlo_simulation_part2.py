
import numpy as np
import matplotlib.pyplot as plt

# Constants
sigma = 0.01  # short rate volatility
T = 5  # 5 years
delta_t = 1/12  # sampling once a month
num_paths = 100  # number of simulated paths
num_steps = int(T/delta_t)  # number of steps
b = 0  # long-term mean rate
r0 = 0.01  # initial short rate

# Array of mean reversion speeds
a_values = np.array([0.2, 0.4, 0.6, 0.8, 1.0])

# Initialize the array to store the paths
paths = np.zeros((len(a_values), num_steps + 1, num_paths))

# Simulate the paths
np.random.seed(42)  # for reproducibility
for i, a in enumerate(a_values):
    paths[i, 0, :] = r0
    for t in range(1, num_steps + 1):
        brownian = np.random.standard_normal(num_paths)
        paths[i, t, :] = paths[i, t - 1, :] + a * (b - paths[i, t - 1, :]) * delta_t + sigma * np.sqrt(delta_t) * brownian

# Plot the first 10 simulated short rate paths for each mean reversion speed
plt.figure(figsize=(10, 6))
for i, a in enumerate(a_values):
    for j in range(10):
        plt.plot(paths[i, :, j], label=f'a = {a}' if j == 0 else '')
plt.title('First 10 Simulated Short Rate Paths for Each Mean Reversion Speed')
plt.xlabel('Time Steps')
plt.ylabel('Short Rate')
plt.legend()
plt.show()

# Zero drift Vasicek model parameters
a_zero = 0
b_zero = 0

# Initialize the array to store the paths
paths_zero = np.zeros((num_steps + 1, num_paths))

# Simulate the paths
np.random.seed(42)  # for reproducibility
paths_zero[0, :] = r0
for t in range(1, num_steps + 1):
    brownian = np.random.standard_normal(num_paths)
    paths_zero[t, :] = paths_zero[t - 1, :] + a_zero * (b_zero - paths_zero[t - 1, :]) * delta_t + sigma * np.sqrt(delta_t) * brownian

# Plot the first 10 simulated short rate paths for the zero drift Vasicek model
plt.figure(figsize=(10, 6))
for i in range(10):
    plt.plot(paths_zero[:, i])
plt.title('First 10 Simulated Short Rate Paths for Zero Drift Vasicek Model')
plt.xlabel('Time Steps')
plt.ylabel('Short Rate')
plt.show()

# Constants for the interest rate cap calculation
loan_amount = 5e6  # 5 million SEK
cap_rate = 0.02  # 2% cap rate
bank_fee = 0.01  # 1% bank fee above the short rate

# Compute the expected payments for each path and each time step
expected_payments = np.maximum(paths_zero - (cap_rate - bank_fee), 0) * loan_amount * delta_t

# The cost of the cap is the sum of the expected payments
cap_cost = np.sum(expected_payments)

cap_cost
