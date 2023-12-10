import numpy as np
from mobility import RandomWaypointModel
from lifi import LifiAccessPoint
from wifi import WiFiAccessPoint
from user import User
import math
from matplotlib import cm
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 

# Function to calculate H(W), H(L1), H(L2), H(L3), and H(L4) for a given point
def calculate_channel_gains(x, y):
    fc = 2.4e9
    user = User(user_id='U', position=(x, y, 0.8))
    H_W = wifi_ap.calculate_channel_gain(user, fc)
    H_L1 = lifi_aps[0].get_channel_gain(x, y)
    H_L2 = lifi_aps[1].get_channel_gain(x, y)
    H_L3 = lifi_aps[2].get_channel_gain(x, y)
    H_L4 = lifi_aps[3].get_channel_gain(x, y)
    return H_W, H_L1, H_L2, H_L3, H_L4

def my_ceil(a, precision=0):
    return np.round(a + 0.5 * 10**(-precision), precision)

def my_floor(a, precision=0):
    return np.round(a - 0.5 * 10**(-precision), precision)

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
print()
print("Grid points:")
print(list(zip(x_grid, y_grid)))
# WiFi access point parameters
wifi_ap = WiFiAccessPoint(ap_id='W', ap_position=(2.5, 2.5, 5), transmit_power=1e-3, noise_psd=10**(-174/10), bandwidth=20e6, sigma=10)

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

# Initialize h_values_matrix as a 3D NumPy array filled with zeros
h_values_matrix = np.zeros((len(x_grid), len(y_grid), 5))

# Populate h_values_matrix from h_values dictionary
for i, x in enumerate(x_grid):
    for j, y in enumerate(y_grid):
        square_h_values = h_values.get((x, y), {'H_W': 0, 'H_L1': 0, 'H_L2': 0, 'H_L3': 0, 'H_L4': 0})
        for k, key in enumerate(['H_W', 'H_L1', 'H_L2', 'H_L3', 'H_L4']):
            h_values_matrix[i, j, k] = square_h_values[key]

with open('H_values_L1_matrix.txt', 'w') as f:
    for a in range(len(x_grid)):
        f.write(f'    {x_grid[a]}')
    f.write('\n')
    for a in range(len(x_grid)):
        f.write(f'{x_grid[a]} ')
        for b in range(len(x_grid)):
            if h_values_matrix[a][b][1] > 0:
                f.write(f' {h_values_matrix[a][b][1]:.3f} ')
            else:
                f.write(f'{h_values_matrix[a][b][1]:.3f} ')
        f.write('\n')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x_grid, y_grid)
# cm.Blues, cm.hsv, cm.coolwarm, cm.gist_rainbow, 
ax.plot_surface(X, Y, 10*np.log10(h_values_matrix[:,:,1]), label='H_L1', alpha=0.6, cmap=cm.coolwarm)
ax.plot_surface(X, Y, 10*np.log10(h_values_matrix[:,:,2]), label='H_L1', alpha=0.6, cmap=cm.coolwarm)
ax.plot_surface(X, Y, 10*np.log10(h_values_matrix[:,:,3]), label='H_L1', alpha=0.6, cmap=cm.coolwarm)
ax.plot_surface(X, Y, 10*np.log10(h_values_matrix[:,:,4]), label='H_L1', alpha=0.6, cmap=cm.coolwarm)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('H_L1')
plt.show()