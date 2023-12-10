import math

class ConventionalMethod:
    chi_factor = 1
    
    # choosen_network:
    # 0: wifi
    # 1: lifi

    def __init__(self, chosen_network, shannon_capacity, proportion_of_time):
        self.name = 'conventional-method'
        self.chosen_network = chosen_network
        self.shannon_capacity = shannon_capacity
        self.proportion_of_time = proportion_of_time
        
    def avg_throughput(self):
        ans = self.chi_factor*self.proportion_of_time*self.shannon_capacity

        return ans