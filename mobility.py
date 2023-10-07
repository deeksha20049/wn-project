import random
import math

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

    def updatePositions(self, time_step):
        if self.pause_time > 0:
            self.pause_time -= time_step
        else:
            distance = math.sqrt(math.pow((self.target_x-self.current_x),2) + math.pow((self.target_y-self.current_y),2))
            if distance > 0:
                self.speed = random.uniform(0, self.max_speed)
                ratio = self.speed / distance
                self.current_x += (self.target_x - self.current_x) * ratio
                self.current_y += (self.target_y - self.current_y) * ratio

            self.pause_time = random.uniform(self.min_pause, self.max_pause)
            self.target_x = random.uniform(0, self.area_width)
            self.target_y = random.uniform(0, self.area_height)