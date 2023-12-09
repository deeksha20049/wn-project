import numpy as np

class User:
    def __init__(self, x, y, mobility_model_params):
        self.x = x
        self.y = y
        self.mobility_model_params = mobility_model_params

    def move(self):
        # Update user position based on the chosen mobility model
        mobility_model = self.mobility_model_params['type']

        if mobility_model == 'random_walk':
            # Random Walk model
            step_size = self.mobility_model_params['step_size']
            angle = np.random.uniform(0, 2 * np.pi)
            self.x += step_size * np.cos(angle)
            self.y += step_size * np.sin(angle)

        # Add more mobility models as needed

        # Ensure the user stays within the room boundaries
        self.x = np.clip(self.x, 0, self.mobility_model_params['room_x'])
        self.y = np.clip(self.y, 0, self.mobility_model_params['room_y'])

if __name__ == "__main__":
    # User mobility model parameters
    mobility_model_params = {
        'type': 'random_walk',  # Change this to the desired mobility model
        'step_size': 0.1,  # Adjust step size based on the room dimensions
        'room_x': 5,
        'room_y': 5,
    }

    # Create a user with initial position
    user = User(x=2.5, y=2.5, mobility_model_params=mobility_model_params)

    # Simulate user movement for a certain number of steps
    num_steps = 100

    for _ in range(num_steps):
        user.move()
        # Perform any necessary calculations or actions based on user's new position
        # For example, calculate throughput or handover decisions

        # Print the user's current position
        print(f"User Position: ({user.x:.2f}, {user.y:.2f})")
