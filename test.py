import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, uniform, poisson

# Parameters
mean_occurrence_rate = 10  # Mean of the occurrence rate (λ)
shape_factor = 1  # Shape factor for Gamma distribution
uniform_min = 0  # Minimum value for uniform distribution
uniform_max = 1  # Maximum value for uniform distribution

# Simulate Gamma-distributed occurrence rate
occurrence_rate = gamma.rvs(shape_factor, scale=1/mean_occurrence_rate, size=1000)

# Simulate uniformly distributed occupation rate
occupation_rate = uniform.rvs(loc=uniform_min, scale=uniform_max, size=1000)

# Simulate Poisson point process
blockage_events = poisson.rvs(occurrence_rate * occupation_rate)

# Set a threshold to obtain a binary indicator
blockage_indicator = (blockage_events > 0).astype(int)

# Plot histograms
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.hist(occurrence_rate, bins=30, density=True, alpha=0.7, color='blue')
plt.title('Gamma-distributed Occurrence Rate')
plt.xlabel('Rate')
plt.ylabel('Probability Density')

plt.subplot(1, 3, 2)
plt.hist(occupation_rate, bins=30, density=True, alpha=0.7, color='green')
plt.title('Uniformly Distributed Occupation Rate')
plt.xlabel('Occupation Rate')
plt.ylabel('Probability Density')

plt.subplot(1, 3, 3)
plt.hist(blockage_indicator, bins=[-0.5, 0.5, 1.5], density=True, alpha=0.7, color='red')
plt.title('Blockage Indicator')
plt.xlabel('Blockage Presence (0: No, 1: Yes)')
plt.ylabel('Probability Density')

plt.tight_layout()
plt.show()
