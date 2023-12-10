import numpy as np
from mobility import RandomWaypointModel
from lifi import LifiAccessPoint
from wifi import WiFiAccessPoint
from user import User
import math
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 

# Function to calculate H(W), H(L1), H(L2), H(L3), and H(L4) for a given point
def calculate_snr(x, y):
    fc = 2.4e9
    user = User(user_id='U', position=(x, y, 0.8))
    snr_W = wifi_ap.calculate_snr(wifi_ap.calculate_channel_gain(user, fc))
    snr_L1 = lifi_aps[0].signal_to_noise_ratio(x, y, otherLifiAPs=lifi_aps[1:])
    # snr_L2 = lifi_aps[1].signal_to_noise_ratio(x, y, otherLifiAPs=lifi_aps[:1] + lifi_aps[2:])
    # snr_L3 = lifi_aps[2].signal_to_noise_ratio(x, y, otherLifiAPs=lifi_aps[:2] + lifi_aps[3:])
    # snr_L4 = lifi_aps[3].signal_to_noise_ratio(x, y, otherLifiAPs=lifi_aps[:3])
    snr_L2, snr_L3, snr_L4 = 0, 0, 0
    return snr_W, snr_L1, snr_L2, snr_L3, snr_L4

def my_ceil(a, precision=0):
    return np.round(a + 0.5 * 10**(-precision), precision)

def my_floor(a, precision=0):
    return np.round(a - 0.5 * 10**(-precision), precision)

def bilinear_interpolation(x, y, snr_values):
    # Check if the user's position is within the grid
    if (x, y) in snr_values:
        return snr_values[(x, y)]
    else:
        # Find the four nearest grid points
        x1, x2 = my_floor(x,1), my_ceil(x,1)
        y1, y2 = my_floor(y,1), my_ceil(y,1)

        # Get the snr at the four nearest grid points
        values_at_x1y1 = snr_values.get((x1, y1), {'snr_W': 0, 'snr_L1': 0, 'snr_L2': 0, 'snr_L3': 0, 'snr_L4': 0})
        values_at_x1y2 = snr_values.get((x1, y2), {'snr_W': 0, 'snr_L1': 0, 'snr_L2': 0, 'snr_L3': 0, 'snr_L4': 0})
        values_at_x2y1 = snr_values.get((x2, y1), {'snr_W': 0, 'snr_L1': 0, 'snr_L2': 0, 'snr_L3': 0, 'snr_L4': 0})
        values_at_x2y2 = snr_values.get((x2, y2), {'snr_W': 0, 'snr_L1': 0, 'snr_L2': 0, 'snr_L3': 0, 'snr_L4': 0})

        # Extract individual components for interpolation
        snrW_1, snrL1_1, snrL2_1, snrL3_1, snrL4_1 = values_at_x1y1.values()
        snrW_2, snrL1_2, snrL2_2, snrL3_2, snrL4_2 = values_at_x1y2.values()
        snrW_3, snrL1_3, snrL2_3, snrL3_3, snrL4_3 = values_at_x2y1.values()
        snrW_4, snrL1_4, snrL2_4, snrL3_4, snrL4_4 = values_at_x2y2.values()

        # Bilinear interpolation for snr_W
        snr_W = (1 / ((x2 - x1) * (y2 - y1))) * (
            snrW_1 * (x2 - x) * (y2 - y) +
            snrW_2 * (x2 - x) * (y - y1) +
            snrW_3 * (x - x1) * (y2 - y) +
            snrW_4 * (x - x1) * (y - y1)
        )

        # Bilinear interpolation for snr_L1
        snr_L1 = (1 / ((x2 - x1) * (y2 - y1))) * (
            snrL1_1 * (x2 - x) * (y2 - y) +
            snrL1_2 * (x2 - x) * (y - y1) +
            snrL1_3 * (x - x1) * (y2 - y) +
            snrL1_4 * (x - x1) * (y - y1)
        )

        # Implement bilinear interpolation for other H values similarly
        # Bilinear interpolation for snr_L2
        snr_L2 = (1 / ((x2 - x1) * (y2 - y1))) * (
            snrL2_1 * (x2 - x) * (y2 - y) +
            snrL2_2 * (x2 - x) * (y - y1) +
            snrL2_3 * (x - x1) * (y2 - y) +
            snrL2_4 * (x - x1) * (y - y1)
        )
        
        # Bilinear interpolation for snr_L3
        snr_L3 = (1 / ((x2 - x1) * (y2 - y1))) * (
            snrL3_1 * (x2 - x) * (y2 - y) +
            snrL3_2 * (x2 - x) * (y - y1) +
            snrL3_3 * (x - x1) * (y2 - y) +
            snrL3_4 * (x - x1) * (y - y1)
        )
        
        # Bilinear interpolation for snr_L4
        snr_L4 = (1 / ((x2 - x1) * (y2 - y1))) * (
            snrL4_1 * (x2 - x) * (y2 - y) +
            snrL4_2 * (x2 - x) * (y - y1) +
            snrL4_3 * (x - x1) * (y2 - y) +
            snrL4_4 * (x - x1) * (y - y1)
        )

        return {
            'snr_W': snr_W,
            'snr_L1': snr_L1,
            'snr_L2': snr_L2,
            'snr_L3': snr_L3,
            'snr_L4': snr_L4
        }


# Room dimensions
room_width = 5.0
room_height = 5.0

# Divide the floor into 0.1x0.1m squares
grid_size = 0.1
x_grid = [round(i * grid_size, 1) for i in range(int(room_width / grid_size) + 1)]
y_grid = [round(i * grid_size, 1) for i in range(int(room_height / grid_size) + 1)]

print(f"Number of squares in x-direction: {len(x_grid)}")
print(f"Number of squares in y-direction: {len(y_grid)}")
print(f"Total number of squares: {len(x_grid) * len(y_grid)}")

# WiFi access point parameters
wifi_ap = WiFiAccessPoint(ap_id='W', ap_position=(2.5, 2.5, 5), transmit_power=0.1, noise_psd=10**((-174 - 30)/10), bandwidth=20e6, sigma=10)

# LiFi access points parameters
lifi_aps = [
    LifiAccessPoint(x=2.5, y=2.5),
    LifiAccessPoint(x=1.25, y=3.75),
    LifiAccessPoint(x=3.75, y=3.75),
    LifiAccessPoint(x=3.75, y=1.25)
]


# Create a dictionary to store snr values for each square
snr_values = {}

# Calculate snr values for each square on the floor
for x in x_grid:
    for y in y_grid:
        snr_W, snr_L1, snr_L2, snr_L3, snr_L4 = calculate_snr(x, y)
        snr_values[(x, y)] = {
            'snr_W': snr_W,
            'snr_L1': snr_L1,
            'snr_L2': snr_L2,
            'snr_L3': snr_L3,
            'snr_L4': snr_L4
        }

# Initialize snr_values_matrix as a 3D NumPy array filled with zeros
snr_values_matrix = np.zeros((len(x_grid), len(y_grid), 5))

# Populate snr_values_matrix from snr_values dictionary
for i, x in enumerate(x_grid):
    for j, y in enumerate(y_grid):
        square_snr_values = snr_values.get((x, y), {'snr_W': 0, 'snr_L1': 0, 'snr_L2': 0, 'snr_L3': 0, 'snr_L4': 0})
        for k, key in enumerate(['snr_W', 'snr_L1', 'snr_L2', 'snr_L3', 'snr_L4']):
            snr_values_matrix[i, j, k] = 10 * np.log10(square_snr_values[key])


# Create a figure and a 3D axis for the surface plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create X and Y mesh grids for plotting
X, Y = np.meshgrid(x_grid, y_grid)

# Create Z values for each channel
Z_snr_W = snr_values_matrix[:, :, 0]  # snr_W
Z_snr_L1 = snr_values_matrix[:, :, 1]  # snr_L1
Z_snr_L2 = snr_values_matrix[:, :, 2]  # snr_L2
Z_snr_L3 = snr_values_matrix[:, :, 3]  # snr_L3
Z_snr_L4 = snr_values_matrix[:, :, 4]  # snr_L4

# Create the surface plots for each channel
# ax.plot_surface(X, Y, Z_snr_W, label='snr_W', alpha=1)
ax.plot_surface(X, Y, Z_snr_L1, label='snr_L1', alpha=0.5)
ax.plot_surface(X, Y, Z_snr_L2, label='snr_L2', alpha=0.5)
ax.plot_surface(X, Y, Z_snr_L3, label='snr_L3', alpha=0.5)
ax.plot_surface(X, Y, Z_snr_L4, label='snr_L4', alpha=0.5)

# Set labels for the axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('SNR')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x_grid, y_grid)
ax.plot_surface(X, Y, Z_snr_W, label='snr_W', alpha=1)
plt.show()