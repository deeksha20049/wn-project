import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, uniform, poisson
import random


def check_blockage(mean_occurrence_rate=1/10, shape_factor=1, uniform_min=0, uniform_max=1):
    # mean_occurrence_rate = 1/10  # Mean of the occurrence rate (λ)
    # shape_factor = 1  # Shape factor for Gamma distribution
    # uniform_min = 0  # Minimum value for uniform distribution
    # uniform_max = 1  # Maximum value for uniform distribution

    # Simulate Gamma-distributed occurrence rate
    occurrence_rate = gamma.rvs(shape_factor, scale=1/mean_occurrence_rate, size=1000000)

    # Simulate uniformly distributed occupation rate
    occupation_rate = uniform.rvs(loc=uniform_min, scale=uniform_max, size=1000000)

    # Simulate Poisson point process
    blockage_events = poisson.rvs(occurrence_rate * occupation_rate)
    
    # Set a threshold to obtain a binary indicator
    blockage_indicator = (blockage_events > 0).astype(int)

    # count values in blockage_indicator
    unique, counts = np.unique(blockage_indicator, return_counts=True)

    # find the probability of blockage
    prob_blockage = counts[1]/(counts[0]+counts[1])    
    return prob_blockage



def generate_random_variable(prob_blockage):
    options = [1, 0]
    probabilities = [prob_blockage, 1 - prob_blockage]
    result = random.choices(options, weights=probabilities, k=1)
    return result[0]


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
