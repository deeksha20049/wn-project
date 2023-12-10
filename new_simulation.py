# IMPORTS
from lifi import LifiAccessPoint
from wifi import WiFiAccessPoint
from propose import ProposedMethod
from conventional import ConventionalMethod
from new_mobility import Mobility
from user import User
from blockage import check_blockage, generate_random_variable

import matplotlib.pyplot as plt
import numpy as np

###

# In meters
ROOM_WIDTH = 5.0
ROOM_HEIGHT = 5.0
USER_HEIGHT = 0.8

GRID_SIZE = 0.1

X_GRID = [round(i * GRID_SIZE, 1) for i in range(int(ROOM_WIDTH / GRID_SIZE) + 1)]
Y_GRID = [round(i * GRID_SIZE, 1) for i in range(int(ROOM_HEIGHT / GRID_SIZE) + 1)]

WIFI_AP = WiFiAccessPoint(ap_id='W', ap_position=(2.5, 2.5, 5), transmit_power=1e-3, noise_psd=10**(-174/10), bandwidth=20e6, sigma=10)

LIFI_APS = [
    LifiAccessPoint(x=1.25, y=1.25),
    LifiAccessPoint(x=1.25, y=3.75),
    LifiAccessPoint(x=3.75, y=3.75),
    LifiAccessPoint(x=3.75, y=1.25)
]

MOBILITY_CONFIG = {
    'type': 'random_walk',
    'step_size': 0.5,
    'room_x': ROOM_WIDTH,
    'room_y': ROOM_HEIGHT
}

NUMBER_OF_USERS = 10

# Lists to store throughput for each user
conventional_throughputs = []
proposed_throughputs = []

for user_index in range(NUMBER_OF_USERS):

    USER = Mobility(0, 0, MOBILITY_CONFIG)

    blockage_prob = check_blockage(mean_occurrence_rate=1/10)

    wifi_snrs = []
    wifi_proportion_time = 0
    lifi_snrs = []
    lifi_propotion_time = 0

    for _ in range(10):
        USER.move()
        print(f"User {user_index+1} Position: ({USER.x:.2f}, {USER.y:.2f})")

        # Calculate WiFi channel gain
        user = User('U', (USER.x, USER.y, USER_HEIGHT))
        wifi_channel_gain = WIFI_AP.calculate_channel_gain(user, fc=2.4e9)
        wifi_snr = WIFI_AP.calculate_snr(wifi_channel_gain)

        # Calculate LiFi channel gains
        blockage_present = [generate_random_variable(blockage_prob) for _ in LIFI_APS] 
        lifi_snr = []
        for i in range(len(LIFI_APS)):
            if blockage_present[i] == 1:
                print(f"Blockage present from LiFi AP {i+1}")
                lifi_snr.append(10*np.log10(LIFI_APS[i].signal_to_noise_ratio_nlos(USER.x, USER.y)))
            else:
                lifi_snr.append(10*np.log10(LIFI_APS[i].signal_to_noise_ratio(USER.x, USER.y)))

        
        print(f"WiFi SNR: {wifi_snr} dB, LiFi SNRs: {lifi_snr}")
        
        if wifi_snr > max(lifi_snr):
            best_router = 'H_W'
            wifi_snrs.append(wifi_snr)
            wifi_proportion_time += 1
        else:
            best_router = max([(lifi_snr[i], f'H_L{i+1}') for i in range(len(lifi_snr))], key=lambda x: x[0])[1]
            lifi_snrs.append(max(lifi_snr))
            lifi_propotion_time += 1

        # Connect the user to the best router based on the decision
        if best_router == 'H_W':
            print("Connecting to WiFi (W)")
        else:
            # Extract the router number from the key (e.g., 'H_L1' -> 'L1')
            router_number = best_router.split('_')[1]
            print(f"Connecting to LiFi ({router_number})")

    # calculate average throughput
    wifi_avg_throughput_proposed = ProposedMethod(0, wifi_snrs, wifi_proportion_time).avg_throughput()
    lifi_avg_throughput_proposed = ProposedMethod(1, lifi_snrs, lifi_propotion_time).avg_throughput()
    wifi_avg_throughput_conventional = ConventionalMethod(0, wifi_snrs, wifi_proportion_time).avg_throughput()
    lifi_avg_throughput_conventional = ConventionalMethod(1, lifi_snrs, lifi_propotion_time).avg_throughput()
    print("Conventional Average Throughput (Mbps): ", (wifi_avg_throughput_conventional + lifi_avg_throughput_conventional)/3000)
    print("Proposed Average Throughput (Mbps): ", (wifi_avg_throughput_proposed + lifi_avg_throughput_proposed)/4000)

    # Append the throughput for this user to the list
    conventional_throughputs.append((wifi_avg_throughput_conventional + lifi_avg_throughput_conventional)/3000)
    proposed_throughputs.append((wifi_avg_throughput_proposed + lifi_avg_throughput_proposed)/4000)

# Calculate overall average throughput across all users
avg_conventional_throughput = np.mean(conventional_throughputs)
avg_proposed_throughput = np.mean(proposed_throughputs)

print("Conventional Overall Average Throughput (Mbps): ", avg_conventional_throughput)
print("Proposed Overall Average Throughput (Mbps): ", avg_proposed_throughput)
