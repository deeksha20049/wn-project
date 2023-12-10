import numpy as np

class Mobility:
    def __init__(self, x, y, mobility_model_params):
        self.x = x
        self.y = y
        self.mobility_model_params = mobility_model_params
        self.target_x = np.random.uniform(0, mobility_model_params['room_x'])
        self.target_y = np.random.uniform(0, mobility_model_params['room_y'])
        self.remaining_time = 0

    def move(self):
        # Update user position based on the chosen mobility model
        mobility_model = self.mobility_model_params['type']

        if mobility_model == 'random_walk':
            # Random Walk model
            step_size = self.mobility_model_params['step_size']
            angle = np.random.uniform(0, 2 * np.pi)
            self.x += step_size * np.cos(angle)
            self.y += step_size * np.sin(angle)

        elif mobility_model == 'random_waypoint':
            if self.remaining_time <= 0:
                # Choose a new random target location
                self.target_x = np.random.uniform(0, self.mobility_model_params['room_x'])
                self.target_y = np.random.uniform(0, self.mobility_model_params['room_y'])
                distance = np.sqrt((self.target_x - self.x)**2 + (self.target_y - self.y)**2)
                self.remaining_time = distance / self.mobility_model_params['speed']

            # Move towards the target location
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance_to_move = min(self.mobility_model_params['speed'], np.sqrt(dx**2 + dy**2))
            angle = np.arctan2(dy, dx)
            self.x += distance_to_move * np.cos(angle)
            self.y += distance_to_move * np.sin(angle)
            self.remaining_time -= 1

        # Add more mobility models as needed

        # Ensure the user stays within the room boundaries
        self.x = np.clip(self.x, 0, self.mobility_model_params['room_x'])
        self.y = np.clip(self.y, 0, self.mobility_model_params['room_y'])

if __name__ == "__main__":
    # User mobility model parameters
    mobility_model_params_random_walk = {
        'type': 'random_walk',
        'step_size': 0.1,
        'room_x': 5,
        'room_y': 5,
    }

    mobility_model_params_random_waypoint = {
        'type': 'random_waypoint',
        'speed': 0.1,
        'room_x': 5,
        'room_y': 5,
    }

    # Create a user with initial position using the desired mobility model
    user = Mobility(x=2.5, y=2.5, mobility_model_params=mobility_model_params_random_waypoint)

    # Simulate user movement for a certain number of steps
    num_steps = 100

    for _ in range(num_steps):
        user.move()
        # Perform any necessary calculations or actions based on the user's new position
        # For example, calculate throughput or handover decisions

        # Print the user's current position
        print(f"User Position: ({user.x:.2f}, {user.y:.2f})")
