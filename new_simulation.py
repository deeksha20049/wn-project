# IMPORTS
from lifi import LifiAccessPoint
from wifi import WiFiAccessPoint
from propose import ProposedMethod
from new_mobility import Mobility
from user import User

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
    'step_size': 0.1,
    'room_x': ROOM_WIDTH,
    'room_y': ROOM_HEIGHT
}

USER = Mobility(0, 0, MOBILITY_CONFIG)

for _ in range(10):
    USER.move()
    print(f"User Position: ({USER.x:.2f}, {USER.y:.2f})")