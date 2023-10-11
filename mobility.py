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
        self.target_x = random.choice([i for i in range(0, int(area_width)) if int(i) != int(self.current_x)])
        self.target_y = random.choice([i for i in range(0, int(area_height)) if int(i) != int(self.current_y)])

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
            self.target_x = random.choice([i for i in range(0, int(self.area_width)) if int(i) != int(self.current_x)])
            self.target_y = random.choice([i for i in range(0, int(self.area_height)) if int(i) != int(self.current_y)])

    def get_position(self):
        return self.current_x, self.current_y

'''
example code to test class
'''

def test():
    area_width = 100  # width of the simulation area
    area_height = 100  # height of the simulation area
    max_speed = 5  # maximum speed of the user/device
    min_pause = 10  # minimum pause time at each stop
    max_pause = 50  # maximum pause time at each stop

    model = RandomWaypointModel(area_width, area_height, max_speed, min_pause, max_pause)

    # Simulating the movement by certain time steps
    for _ in range(100):
        model.update(1)  # Updating time step by 1s
        x, y = model.get_position()
        print(f"Current Position: ({x}, {y})")

if __name__  == "__main__":
    test()

