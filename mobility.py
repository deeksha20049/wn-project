import random

class RandomWaypointModel:
    def __init__(self, area_width, area_height, max_speed, min_pause, max_pause):
        self.area_width = area_width
        self.area_height = area_height
        self.max_speed = max_speed
        self.min_pause = min_pause
        self.max_pause = max_pause
        self.current_x = random.uniform(0, area_width)
        self.current_y = random.uniform(0, area_height)
        self.target_x = random.uniform(0, area_width)
        self.target_y = random.uniform(0, area_height)
        self.speed = 0
        self.pause_time = 0

    