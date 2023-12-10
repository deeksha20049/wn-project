import math

class ConventionalMethod:
    chi_factor = 1

    bw = 20 # MHz

    proportion_of_time = 1.0

    # choosen_network:
    # 0: wifi
    # 1: lifi

    def __init__(self, chosen_network, snr_list):
        self.name = 'convetional-method'
        self.chosen_network = chosen_network
        self.snr_list = snr_list
        self.shannon_capacity_list = self.shannon_capacity(self.snr_list)
    
    def shannon_capacity(self, snr_list):
        shannon_capacity_list = []
        for snr in snr_list:
            shannon_capacity_list.append(self.bw*math.log2(1 + snr))
        return shannon_capacity_list
    
    def avg_throughput(self):
        if (self.chosen_network == 1):
            ans = 0
            for i in range(len(self.snr_list)):
                ans += self.chi_factor*self.proportion_of_time*self.shannon_capacity_list[i]

        elif (self.chosen_network == 0):
            ans = 0
            for i in range(len(self.snr_list)):
                ans += self.chi_factor*self.proportion_of_time*self.shannon_capacity_list[i]

        return ans