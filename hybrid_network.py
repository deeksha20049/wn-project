from lifi import LifiAccessPoint
from wifi import WiFiAccessPoint
from user import User
import numpy as np
from scipy.optimize import minimize

class HybridNetworkOptimizer:
    def __init__(self, lifi_aps, wifi_ap, users):
        self.lifi_aps = {user: lifi_ap for user, lifi_ap in zip(users, lifi_aps)}
        self.wifi_ap = wifi_ap
        self.users = users

    def objective_function(self, decision_variables):
        total_throughput = 0

        for i, user in enumerate(self.users):
            chosen_network = decision_variables[i]

            if chosen_network == 1:  # LiFi
                channel_gain = self.lifi_aps[user].get_channel_gain(user.position[0], user.position[1])
            else:  # WiFi
                channel_gain = self.wifi_ap.calculate_channel_gain(user, fc=2.4e9)

            throughput = np.log2(1 + channel_gain * self.wifi_ap.transmit_power / self.wifi_ap.noise_psd)
            total_throughput += throughput

        return -total_throughput  # Minimize negative throughput (maximize throughput)

    def constraint_function(self, decision_variables):
        return sum(decision_variables) - len(self.users)  # Ensure each user is assigned to exactly one network

    def optimize_network_selection(self):
        # Initial guess for decision variables
        initial_guess = np.ones(len(self.users))

        # Define optimization problem
        optimization_problem = {
            'method': 'SLSQP',
            'fun': self.objective_function,
            'constraints': {'type': 'eq', 'fun': self.constraint_function}
        }

        # Run optimization
        result = minimize(self.objective_function, initial_guess, constraints=optimization_problem['constraints'], method=optimization_problem['method'])

        # Extract optimized decision variables
        optimized_decision_variables = result.x

        # Use the optimized decision variables to update network selection for each user
        for i, user in enumerate(self.users):
            chosen_network = optimized_decision_variables[i]

            if chosen_network == 1:  # LiFi
                print(f"User {user.user_id} is assigned to LiFi.")
            else:  # WiFi
                print(f"User {user.user_id} is assigned to WiFi.")

        return optimized_decision_variables


# Example usage:
if __name__ == "__main__":
    lifi_ap1 = LifiAccessPoint(x=1.25, y=1.25)
    lifi_ap2 = LifiAccessPoint(x=1.25, y=3.75)
    lifi_ap3 = LifiAccessPoint(x=3.75, y=3.75)
    lifi_ap4 = LifiAccessPoint(x=3.75, y=1.25)

    # wifi_ap = WiFiAccessPoint(ap_id=1, ap_position=(2.5, 2.5), transmit_power=1e-3 * 10**(20/10), noise_psd=10**(-174/10), bandwidth=20e6, sigma=10)
    wifi_ap = WiFiAccessPoint(ap_id=1, ap_position=(2.5, 2.5), transmit_power=1e-3, noise_psd=10**(-174/10), bandwidth=20e6, sigma=10)

    user1 = User(user_id=1, position=(1.25, 1.25))
    user2 = User(user_id=2, position=(1, 1))
    user3 = User(user_id=3, position=(3, 4))

    optimizer = HybridNetworkOptimizer(lifi_aps=[lifi_ap1, lifi_ap2, lifi_ap3, lifi_ap4], wifi_ap=wifi_ap, users=[user1, user2, user3])

    optimized_decisions = optimizer.optimize_network_selection()
    
    
    
# https://chat.openai.com/share/c43948ed-f435-48cf-a450-d3d3c975b45e