# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import gamma, uniform, poisson

# # Parameters
# mean_occurrence_rate = 30  # Mean of the occurrence rate (λ)
# shape_factor = 1  # Shape factor for Gamma distribution
# uniform_min = 0  # Minimum value for uniform distribution
# uniform_max = 1  # Maximum value for uniform distribution

# # Simulate Gamma-distributed occurrence rate
# occurrence_rate = gamma.rvs(shape_factor, scale=1/mean_occurrence_rate, size=1000000)

# # Simulate uniformly distributed occupation rate
# occupation_rate = uniform.rvs(loc=uniform_min, scale=uniform_max, size=1000000)

# # Simulate Poisson point process
# blockage_events = poisson.rvs(occurrence_rate * occupation_rate)
# print(blockage_events)
# # Set a threshold to obtain a binary indicator
# blockage_indicator = (blockage_events > 0).astype(int)

# # Plot histograms
# plt.figure(figsize=(12, 4))

# plt.subplot(1, 3, 1)
# plt.hist(occurrence_rate, bins=30, density=True, alpha=0.7, color='blue')
# plt.title('Gamma-distributed Occurrence Rate')
# plt.xlabel('Rate')
# plt.ylabel('Probability Density')

# plt.subplot(1, 3, 2)
# plt.hist(occupation_rate, bins=30, density=True, alpha=0.7, color='green')
# plt.title('Uniformly Distributed Occupation Rate')
# plt.xlabel('Occupation Rate')
# plt.ylabel('Probability Density')

# plt.subplot(1, 3, 3)
# plt.hist(blockage_indicator, bins=[-0.5, 0.5, 1.5], density=True, alpha=0.7, color='red')
# plt.title('Blockage Indicator')
# plt.xlabel('Blockage Presence (1: No, 0: Yes)')
# plt.ylabel('Probability Density')

# plt.tight_layout()
# plt.show()

room_width = 5.0
room_height = 5.0
user_height = 0.8

# Divide the floor into 0.1x0.1m squares
grid_size = 0.1
# x_grid = np.arange(0, room_width, grid_size)
# y_grid = np.arange(0, room_height, grid_size)
x_grid = [round(i * grid_size, 1) for i in range(int(room_width / grid_size) + 1)]
y_grid = [round(i * grid_size, 1) for i in range(int(room_height / grid_size) + 1)]

print(f"Number of squares in x-direction: {len(x_grid)}")
print(f"Number of squares in y-direction: {len(y_grid)}")
print(f"Total number of squares: {len(x_grid) * len(y_grid)}")
print()
print("Grid points:")
# print(list(zip(x_grid, y_grid)))
# make list of all ombination of x and y
grid_points = [(x, y) for x in x_grid for y in y_grid]
print(grid_points)