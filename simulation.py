import numpy as np
from mobility import RandomWaypointModel
from lifi import LifiAccessPoint
from wifi import WiFiAccessPoint
from user import User
import math
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D 

# Function to calculate H(W), H(L1), H(L2), H(L3), and H(L4) for a given point
def calculate_channel_gains(x, y):
    fc = 2.4e9
    user = User(user_id='U', position=(x, y, user_height))
    H_W = wifi_ap.calculate_channel_gain(user, fc)
    H_L1 = lifi_aps[0].get_channel_gain(x, y)
    H_L2 = lifi_aps[1].get_channel_gain(x, y)
    H_L3 = lifi_aps[2].get_channel_gain(x, y)
    H_L4 = lifi_aps[3].get_channel_gain(x, y)
    return H_W, H_L1, H_L2, H_L3, H_L4

# Function to calculate H(W), H(L1), H(L2), H(L3), and H(L4) for a given point
def calculate_snr(x, y):
    fc = 2.4e9
    user = User(user_id='U', position=(x, y, 0.8))
    H_W = wifi_ap.calculate_channel_gain(user, fc)
    H_L1 = lifi_aps[0].get_channel_gain(x, y)
    H_L2 = lifi_aps[1].get_channel_gain(x, y)
    H_L3 = lifi_aps[2].get_channel_gain(x, y)
    H_L4 = lifi_aps[3].get_channel_gain(x, y)
    snr_W = wifi_ap.calculate_snr(H_W)
    snr_L1 = lifi_aps[0].signal_to_noise_ratio(x, y, otherLifiAPs=lifi_aps[1:])
    snr_L2 = lifi_aps[1].signal_to_noise_ratio(x, y, otherLifiAPs=lifi_aps[:1] + lifi_aps[2:])
    snr_L3 = lifi_aps[2].signal_to_noise_ratio(x, y, otherLifiAPs=lifi_aps[:2] + lifi_aps[3:])
    snr_L4 = lifi_aps[3].signal_to_noise_ratio(x, y, otherLifiAPs=lifi_aps[:3])
    return np.array([H_W, H_L1, H_L2, H_L3, H_L4]), np.array([snr_W, snr_L1, snr_L2, snr_L3, snr_L4])

def my_ceil(a, precision=0):
    return np.round(a + 0.5 * 10**(-precision), precision)

def my_floor(a, precision=0):
    return np.round(a - 0.5 * 10**(-precision), precision)

def bilinear_interpolation(x, y, h_values):
    # Check if the user's position is within the grid
    if (x, y) in h_values:
        return h_values[(x, y)]
    else:
        # Find the four nearest grid points
        x1, x2 = my_floor(x,1), my_ceil(x,1)
        y1, y2 = my_floor(y,1), my_ceil(y,1)
        print(f"({x1}, {y1}), ({x1}, {y2}), ({x2}, {y1}), ({x2}, {y2})")

        # Get the channel gains at the four nearest grid points
        values_at_x1y1 = h_values.get((x1, y1), {'H_W': 0, 'H_L1': 0, 'H_L2': 0, 'H_L3': 0, 'H_L4': 0})
        values_at_x1y2 = h_values.get((x1, y2), {'H_W': 0, 'H_L1': 0, 'H_L2': 0, 'H_L3': 0, 'H_L4': 0})
        values_at_x2y1 = h_values.get((x2, y1), {'H_W': 0, 'H_L1': 0, 'H_L2': 0, 'H_L3': 0, 'H_L4': 0})
        values_at_x2y2 = h_values.get((x2, y2), {'H_W': 0, 'H_L1': 0, 'H_L2': 0, 'H_L3': 0, 'H_L4': 0})

        # Extract individual components for interpolation
        H_W1, H_L1_1, H_L2_1, H_L3_1, H_L4_1 = values_at_x1y1.values()
        H_W2, H_L1_2, H_L2_2, H_L3_2, H_L4_2 = values_at_x1y2.values()
        H_W3, H_L1_3, H_L2_3, H_L3_3, H_L4_3 = values_at_x2y1.values()
        H_W4, H_L1_4, H_L2_4, H_L3_4, H_L4_4 = values_at_x2y2.values()

        # Bilinear interpolation for H_W
        H_W = (1 / ((x2 - x1) * (y2 - y1))) * (
            H_W1 * (x2 - x) * (y2 - y) +
            H_W2 * (x2 - x) * (y - y1) +
            H_W3 * (x - x1) * (y2 - y) +
            H_W4 * (x - x1) * (y - y1)
        )

        # Bilinear interpolation for H_L1
        H_L1 = (1 / ((x2 - x1) * (y2 - y1))) * (
            H_L1_1 * (x2 - x) * (y2 - y) +
            H_L1_2 * (x2 - x) * (y - y1) +
            H_L1_3 * (x - x1) * (y2 - y) +
            H_L1_4 * (x - x1) * (y - y1)
        )

        # Implement bilinear interpolation for other H values similarly
        # Bilinear interpolation for H_L2
        H_L2 = (1 / ((x2 - x1) * (y2 - y1))) * (
            H_L2_1 * (x2 - x) * (y2 - y) +
            H_L2_2 * (x2 - x) * (y - y1) +
            H_L2_3 * (x - x1) * (y2 - y) +
            H_L2_4 * (x - x1) * (y - y1)
        )
        
        # Bilinear interpolation for H_L3
        H_L3 = (1 / ((x2 - x1) * (y2 - y1))) * (
            H_L3_1 * (x2 - x) * (y2 - y) +
            H_L3_2 * (x2 - x) * (y - y1) +
            H_L3_3 * (x - x1) * (y2 - y) +
            H_L3_4 * (x - x1) * (y - y1)
        )
        
        # Bilinear interpolation for H_L4
        H_L4 = (1 / ((x2 - x1) * (y2 - y1))) * (
            H_L4_1 * (x2 - x) * (y2 - y) +
            H_L4_2 * (x2 - x) * (y - y1) +
            H_L4_3 * (x - x1) * (y2 - y) +
            H_L4_4 * (x - x1) * (y - y1)
        )

        return {
            'H_W': H_W,
            'H_L1': H_L1,
            'H_L2': H_L2,
            'H_L3': H_L3,
            'H_L4': H_L4
        }


# Room dimensions
room_width = 5.0
room_height = 5.0
user_height = 0.8

# Divide the floor into 0.1x0.1m squares
grid_size = 0.1
# x_grid = np.arange(0, room_width, grid_size)
# y_grid = np.arange(0, room_height, grid_size)
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

# Create a dictionary to store snr values for each square
snr_values = {}

# Initialize H_values_matrix and snr_values_matrix as a 3D NumPy array filled with zeros
snr_values_matrix = np.zeros((len(x_grid), len(y_grid), 5))
H_values_matrix = np.zeros((len(x_grid), len(y_grid), 5))

# Calculate snr values for each square on the floor
for i, x in enumerate(x_grid):
    for j, y in enumerate(y_grid):
        channel_gains_ret, snr_values_ret = calculate_snr(x, y)
        snr_values[(x, y)] = {
            'snr_W': snr_values_ret[0],
            'snr_L1': snr_values_ret[1],
            'snr_L2': snr_values_ret[2],
            'snr_L3': snr_values_ret[3],
            'snr_L4': snr_values_ret[4]
        }
        H_values_matrix[i, j, :] = channel_gains_ret
        snr_values_matrix[i, j, :] = snr_values_ret

# Convert snr_values_matrix to dB
snr_values_matrix_dB = 10 * np.log10(snr_values_matrix)

# Convert h_values_matrix to dB
H_values_matrix_dB = 10 * np.log10(H_values_matrix)

# # Create a dictionary to store H values for each square
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

# Create a user mobility model
user_model = RandomWaypointModel(room_width, room_height, max_speed=1.0, min_pause=1, max_pause=1)

# Initialize user position at (2.5, 2.5) and height 0.8
user_x, user_y = 0, 0
user_height = 0.8

# print(h_values)
# breakpoint()
# Simulate user's movement and print the updated H values
for _ in range(10):  # Simulate for 10 seconds (10 steps)
    user_model.updatePositions(0.1)  # Move the user every 1 second
    user_x, user_y = user_model.get_position()
    print(f"User at ({user_x:.2f}, {user_y:.2f}), Height: {user_height:.2f}")

    # Get the H values at the user's current position from the precomputed dictionary
    # h_values_at_user_position = h_values.get((round(user_x), round(user_y)))
    # h_values_at_user_position = h_values.get((math.floor(user_x), math.ceil(user_y)))
    # h_values_at_user_position = h_values.get((user_x, user_y))
    
    # Get the estimated H values at the user's current position using bilinear interpolation
    estimated_gains = bilinear_interpolation(user_x, user_y, h_values)
    
    print(f"H(W): {estimated_gains['H_W']}")
    print(f"H(L1): {estimated_gains['H_L1']}")
    print(f"H(L2): {estimated_gains['H_L2']}")
    print(f"H(L3): {estimated_gains['H_L3']}")
    print(f"H(L4): {estimated_gains['H_L4']}")

    # Determine which router has the highest channel gain
    best_router = max(estimated_gains, key=lambda key: estimated_gains[key])
    print(f"Best Router: {best_router}")

    # Connect the user to the best router based on the decision
    if best_router == 'H_W':
        print("Connecting to WiFi (W)")
    else:
        # Extract the router number from the key (e.g., 'H_L1' -> 'L1')
        router_number = best_router.split('_')[1]
        print(f"Connecting to LiFi ({router_number})")

    print()


# for 10 users with 10 diff objects

users = []

for _ in range(10):
    user_model = RandomWaypointModel(room_width, room_height, max_speed=1.0, min_pause=1, max_pause=1)
    user_x, user_y = np.random.uniform(0, room_width), np.random.uniform(0, room_height)
    user_height = 0.8  
    user = User(user_id=f'U{_}', position=(user_x, user_y, user_height))
    users.append((user, user_model))

# Simulate users' movement and calculate H values for each user
for _ in range(10):  # Simulate for 10 seconds
    for user, user_model in users:
        user_model.updatePositions(0.1)  # Move the user every 1 second
        user_x, user_y = user_model.get_position()
        print(f"User {user.user_id} at ({user_x:.2f}, {user_y:.2f}), Height: {user_height:.2f}")

        # Calculate H values and SNR for the current user's position
        H_values, snr_values = calculate_snr(user_x, user_y)

        print(f"H(W): {H_values[0]}")
        print(f"H(L1): {H_values[1]}")
        print(f"H(L2): {H_values[2]}")
        print(f"H(L3): {H_values[3]}")
        print(f"H(L4): {H_values[4]}")

        best_router = np.argmax(snr_values)
        if best_router == 0:
            print("Connecting to WiFi (W)")
        else:
            router_number = best_router
            print(f"Connecting to LiFi ({router_number})")

        print()


# ---

# # Create a user mobility model
# user_model = RandomWaypointModel(room_width, room_height, max_speed=1.0, min_pause=1, max_pause=1)

# # Initialize user position at (2.5, 2.5) and height 0.8
# user_x, user_y = 0, 0
# user_height = 0.8

# # Lists to store user positions for the surface plot
# x_positions = []
# y_positions = []
# z_positions = []

# # Simulate user's movement and print the updated H values
# for _ in range(100):  # Simulate for 100 time steps
#     user_model.updatePositions(0.1)  # Move the user every 0.1 seconds
#     user_x, user_y = user_model.get_position()
#     print(f"User at ({user_x:.2f}, {user_y:.2f}), Height: {user_height:.2f}")

#     # Store user positions
#     x_positions.append(user_x)
#     y_positions.append(user_y)
#     z_positions.append(user_height)

# # Create a 3D surface plot using the captured positions
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_trisurf(x_positions, y_positions, z_positions, cmap='viridis')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Height')
# plt.show()


# Create a figure and a 3D axis for the surface plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Create X and Y mesh grids for plotting
# X, Y = np.meshgrid(x_grid, y_grid)

# # Create Z values for each channel
# Z_H_W = h_values_matrix[:, :, 0]  # H_W
# Z_H_L1 = h_values_matrix[:, :, 1]  # H_L1
# Z_H_L2 = h_values_matrix[:, :, 2]  # H_L2
# Z_H_L3 = h_values_matrix[:, :, 3]  # H_L3
# Z_H_L4 = h_values_matrix[:, :, 4]  # H_L4

# # Create the surface plots for each channel
# ax.plot_surface(X, Y, Z_H_W, cmap='viridis', label='H_W', alpha=0.8)
# ax.plot_surface(X, Y, Z_H_L1, cmap='plasma', label='H_L1', alpha=0.8)
# ax.plot_surface(X, Y, Z_H_L2, cmap='inferno', label='H_L2', alpha=0.8)
# ax.plot_surface(X, Y, Z_H_L3, cmap='magma', label='H_L3', alpha=0.8)
# ax.plot_surface(X, Y, Z_H_L4, cmap='cividis', label='H_L4', alpha=0.8)

# # Set labels for the axes
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Channel Gain')

# # Show the plot
# plt.show()
