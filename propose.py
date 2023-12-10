import math

class ProposedMethod:
    chi_factor = 1
    avg_cell_dwell_time = 0.4478 # T_a_u
    eta = 1.5 # refractive index
    hho = 200 # ms

    # choosen_network:
    # 0: wifi
    # 1: lifi

    def __init__(self, chosen_network, shannon_capacity, proportion_of_time):
        self.name = 'proposed-method'
        self.chosen_network = chosen_network
        self.shannon_capacity = shannon_capacity
        self.proportion_of_time = proportion_of_time
        if (self.chosen_network == 1):
            self.vho = 1 - self.eta
        elif (self.chosen_network == 0):
            self.vho = 0

    def avg_throughput(self):
        if (self.choosen_network == 1):
            ans = self.chi_factor*self.vho*self.shannon_capacity*math.min(self.proportion_of_time, 1 - (self.hho/self.avg_cell_dwell_time))

        elif (self.choosen_network == 0):
            ans = self.chi_factor*self.vho*self.shannon_capacity*self.proportion_of_time

        return ans