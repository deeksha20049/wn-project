import numpy as np

class User:
    def __init__(self, user_id, position):
        self.user_id = user_id
        self.position = position

    def calculate_distance(self, ap_position):
        return np.linalg.norm(np.array(ap_position) - np.array(self.position))