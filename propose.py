import math

class ProposedMethod:
    chi_factor = 1
    # T_a_u = cell dwell time
    eta = 1.5 # refractive index
    hho = 200 # ms
    bw = 20*10 # MHz


    cell_dwell_times = [
        0.4478,
        0.2068,
        0.0013,
        0.5160,
        0.2375,
        0.0004,
        0.3651,
        0.1307,
        0.0003,
        0.3524,
        0.1218,
        0.00006
    ]

    avg_cell_dwell_time = sum(cell_dwell_times)/len(cell_dwell_times)

    # choosen_network:
    # 0: wifi
    # 1: lifi

    def __init__(self, chosen_network, snr_list, proportion_of_time):
        self.name = 'proposed-method'
        self.chosen_network = chosen_network
        self.snr_list = snr_list
        if (self.chosen_network == 1):
            self.vho = 1 - self.eta
        elif (self.chosen_network == 0):
            self.vho = 1
        self.shannon_capacity_list = self.shannon_capacity(self.snr_list)
        self.proportion_of_time = proportion_of_time
    
    def shannon_capacity(self, snr_list):
        shannon_capacity_list = []
        for snr in snr_list:
            shannon_capacity_list.append(self.bw*math.log2(1 + snr))
        return shannon_capacity_list
    
    def avg_throughput(self):
        if (self.chosen_network == 1):
            # ans = self.chi_factor*self.vho*self.shannon_capacity*min(self.proportion_of_time, 1 - (self.hho/self.avg_cell_dwell_time))
            # ans = self.chi_factor * summation (self.vho * self.shannon_capacity_list's element * minimum(self.proportion_of_time, 1 - (self.hho/self.avg_cell_dwell_time)))

            ans = 0
            for i in range(len(self.snr_list)):
                ans += self.chi_factor*self.vho*self.shannon_capacity_list[i]*min(self.proportion_of_time, 1 - (self.hho/self.avg_cell_dwell_time))

        elif (self.chosen_network == 0):
            # ans = self.chi_factor*self.vho*self.shannon_capacity*self.proportion_of_time
            # ans = self.chi_factor * summation (self.vho * self.shannon_capacity_list's element * self.proportion_of_time)

            ans = 0
            for i in range(len(self.snr_list)):
                ans += self.chi_factor*self.vho*self.shannon_capacity_list[i]*self.proportion_of_time

        return ans

if __name__ == "__main__":
    cell_dwell_times = [
        0.4478,
        0.2068,
        0.0013,
        0.5160,
        0.2375,
        0.0004,
        0.3651,
        0.1307,
        0.0003,
        0.3524,
        0.1218,
        0.00006
    ]

    avg_cell_dwell_time = sum(cell_dwell_times)/len(cell_dwell_times)

    print(avg_cell_dwell_time)