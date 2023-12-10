from lifi import LifiAccessPoint
from wifi import WiFiAccessPoint
from propose import ProposedMethod
from conventional import ConventionalMethod
from new_mobility import Mobility
from user import User
from blockage import check_blockage, generate_random_variable

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import Tk, Canvas, Label, Button

# Simulation parameters
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

# Create lists to store user positions for plotting
user_positions_x = [[] for _ in range(NUMBER_OF_USERS)]
user_positions_y = [[] for _ in range(NUMBER_OF_USERS)]

# Create a list to store the best router chosen for each user
best_routers = []

# Create Tkinter window
root = Tk()
root.title("Wireless Communication Simulation")
root.geometry("900x900")

# Create Matplotlib figure
fig, ax = plt.subplots(figsize=(4, 4))

# Create canvas for Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, padx=10, pady=10)

# Create labels and buttons
label_user = Label(root, text="User Movements:")
label_user.grid(row=1, column=0, padx=10, pady=5)

button_next = Button(root, text="Next", command=lambda: update_simulation())
button_next.grid(row=1, column=1, padx=10, pady=5)

# Initialize the users and the simulation
users = [Mobility(np.random.uniform(0, ROOM_WIDTH), np.random.uniform(0, ROOM_HEIGHT), MOBILITY_CONFIG) for _ in range(NUMBER_OF_USERS)]
current_step = 0

def calculate_snrs(user):
    wifi_snrs = []
    lifi_snrs = []
    wifi_proportion_time = 0
    lifi_propotion_time = 0
    best_router = ""

    blockage_prob = check_blockage(mean_occurrence_rate=1/10)

    for _ in range(10):
        user.move()

        # Store user positions for plotting
        user_positions_x[current_step].append(user.x)
        user_positions_y[current_step].append(user.y)

        print(f"User {current_step + 1} Position: ({user.x:.2f}, {user.y:.2f})")

        # Calculate WiFi channel gain
        u = User('U', (user.x, user.y, USER_HEIGHT))
        wifi_channel_gain = WIFI_AP.calculate_channel_gain(u, fc=2.4e9)
        wifi_snr = WIFI_AP.calculate_snr(wifi_channel_gain)

        # Calculate LiFi channel gains
        blockage_present = [generate_random_variable(blockage_prob) for _ in LIFI_APS]
        lifi_snr = []
        for i in range(len(LIFI_APS)):
            if blockage_present[i] == 1:
                print(f"Blockage present from LiFi AP {i + 1}")
                lifi_snr.append(10 * np.log10(LIFI_APS[i].signal_to_noise_ratio_nlos(user.x, user.y)))
            else:
                lifi_snr.append(10 * np.log10(LIFI_APS[i].signal_to_noise_ratio(user.x, user.y)))

        print(f"WiFi SNR: {wifi_snr} dB, LiFi SNRs: {lifi_snr}")

        if wifi_snr > max(lifi_snr):
            best_router = 'H_W'
            wifi_snrs.append(wifi_snr)
            wifi_proportion_time += 1
        else:
            best_router = max([(lifi_snr[i], f'H_L{i + 1}') for i in range(len(lifi_snr))], key=lambda x: x[0])[1]
            lifi_snrs.append(max(lifi_snr))
            lifi_propotion_time += 1

        # Connect the user to the best router based on the decision
        if best_router == 'H_W':
            print("Connecting to WiFi (W)")
        else:
            # Extract the router number from the key (e.g., 'H_L1' -> 'L1')
            router_number = best_router.split('_')[1]
            print(f"Connecting to LiFi ({router_number})")

    return wifi_snrs, lifi_snrs, best_router, wifi_proportion_time, lifi_propotion_time

def update_simulation():
    global current_step
    if current_step < 10:
        user = users[current_step]
        user.move()
        user_positions_x[current_step].append(user.x)
        user_positions_y[current_step].append(user.y)

        # Calculate WiFi and LiFi SNRs
        wifi_snrs, lifi_snrs, best_router, wifi_proportion_time, lifi_propotion_time = calculate_snrs(user)

        # Calculate average throughput
        wifi_avg_throughput_proposed = ProposedMethod(0, wifi_snrs, wifi_proportion_time).avg_throughput()
        lifi_avg_throughput_proposed = ProposedMethod(1, lifi_snrs, lifi_propotion_time).avg_throughput()
        wifi_avg_throughput_conventional = ConventionalMethod(0, wifi_snrs, wifi_proportion_time).avg_throughput()
        lifi_avg_throughput_conventional = ConventionalMethod(1, lifi_snrs, lifi_propotion_time).avg_throughput()

        # Append the throughput for this user to the list
        conventional_throughputs.append((wifi_avg_throughput_conventional + lifi_avg_throughput_conventional) / 3000)
        proposed_throughputs.append((wifi_avg_throughput_proposed + lifi_avg_throughput_proposed) / 4000)

        # Update the best router list
        best_routers.append(best_router)

        # Plot user movements
        ax.clear()
        for i in range(NUMBER_OF_USERS):
            ax.plot(user_positions_x[i], user_positions_y[i], label=f'User {i+1}')
        ax.set_title('User Movements in the Room')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.legend()
        ax.grid(True)

        canvas.draw()

        current_step += 1

# Start the Tkinter main loop
root.mainloop()