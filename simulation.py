import numpy as np
from mobility import RandomWaypointModel
from lifi import LifiAccessPoint
from wifi import WiFiAccessPoint

# Function to calculate H(W), H(L1), H(L2), H(L3), and H(L4) for a given point
def calculate_channel_gains(x, y):
    H_W = wifi_ap.calculate_channel_gain(x, y)
    H_L1 = lifi_aps[0].get_channel_gain(x, y)
    H_L2 = lifi_aps[1].get_channel_gain(x, y)
    H_L3 = lifi_aps[2].get_channel_gain(x, y)
    H_L4 = lifi_aps[3].get_channel_gain(x, y)
    return H_W, H_L1, H_L2, H_L3, H_L4

# Room dimensions
room_width = 5.0
room_height = 5.0

# Divide the floor into 0.1x0.1m squares
grid_size = 0.1
x_grid = np.arange(0, room_width, grid_size)
y_grid = np.arange(0, room_height, grid_size)

# WiFi access point parameters
wifi_ap = WiFiAccessPoint(ap_id='W', ap_position=(2.5, 2.5), transmit_power=1e-3, noise_psd=10**(-174/10), bandwidth=20e6, sigma=10)

# LiFi access points parameters
lifi_aps = [
    LifiAccessPoint(x=1.25, y=1.25),
    LifiAccessPoint(x=1.25, y=3.75),
    LifiAccessPoint(x=3.75, y=3.75),
    LifiAccessPoint(x=3.75, y=1.25)
]

# Create a dictionary to store H values for each square
h_values = {}

# Calculate H values for each square on the floor
for x in x_grid:
    for y in y_grid:
        H_W, H_L1, H_L2, H_L3, H_L4 = calculate_channel_gains(x, y)
        h_values[(x, y)] = {
            'H_W': H_W,
            'H_L1': H_L1,
            'H_L2': H_L2,
            'H_L3': H_L3,
            'H_L4': H_L4
        }

# Print or store the H values for each square as needed
for (x, y), values in h_values.items():
    print(f"Square ({x:.2f}, {y:.2f}):")
    print(f"H(W): {values['H_W']:.4f}")
    print(f"H(L1): {values['H_L1']:.4f}")
    print(f"H(L2): {values['H_L2']:.4f}")
    print(f"H(L3): {values['H_L3']:.4f}")
    print(f"H(L4): {values['H_L4']:.4f}")
    print()
