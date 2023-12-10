# IMPORTS
from lifi import LifiAccessPoint
from wifi import WiFiAccessPoint
from propose import ProposedMethod
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

USER = Mobility(4, 4, MOBILITY_CONFIG)
blockage_prob = check_blockage(mean_occurrence_rate=1/10)

for _ in range(10):
    USER.move()
    print(f"User Position: ({USER.x:.2f}, {USER.y:.2f})")

    # Calculate WiFi channel gain
    user = User('U', (USER.x, USER.y, USER_HEIGHT))
    wifi_channel_gain = WIFI_AP.calculate_channel_gain(user, fc=2.4e9)
    wifi_snr = WIFI_AP.calculate_snr(wifi_channel_gain)

    # Calculate LiFi channel gains
    blockage_present = [generate_random_variable(blockage_prob) for _ in LIFI_APS] 
    lifi_snr = []
    for i in range(len(LIFI_APS)):
        if blockage_present[i] == 1:
            lifi_snr.append(LIFI_APS[i].signal_to_noise_ratio_nlos(USER.x, USER.y))
        else:
            lifi_snr.append(LIFI_APS[i].signal_to_noise_ratio(USER.x, USER.y))
    
    
    # lifi_snr = [10 * np.log10(lifi_ap.signal_to_noise_ratio(USER.x, USER.y)) for lifi_ap in LIFI_APS]
    # lifi_snr = [(1 - blockage_present[i]) * lifi_snr[i] for i in range(len(LIFI_APS))]
    
    
    # # Use the proposed method to determine average throughput
    # proposed_method_wifi = ProposedMethod(chosen_network=0, shannon_capacity=1e6, proportion_of_time=0.8)
    # proposed_method_lifi = ProposedMethod(chosen_network=1, shannon_capacity=1e6, proportion_of_time=0.8)

    # wifi_throughput = proposed_method_wifi.avg_throughput()
    # lifi_throughputs = [proposed_method_lifi.avg_throughput() for _ in LIFI_APS]

    # # Decide the best connection based on the highest gain
    # best_connection = max([(wifi_throughput, 'WiFi')] + list(zip(lifi_throughputs, [f'LiFi_{i+1}' for i in range(len(LIFI_APS))])), key=lambda x: x[0])

    # print(f"WiFi Throughput: {wifi_throughput} bps, LiFi Throughputs: {lifi_throughputs}")
    # print(f"Best Connection: {best_connection[1]} with Throughput: {best_connection[0]} bps\n")
    
    print(f"WiFi SNR: {wifi_snr} dB, LiFi SNRs: {lifi_snr}")