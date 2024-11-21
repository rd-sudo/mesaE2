import mesa
import numpy as np
import random
from TrafficLightAgent import TrafficLightAgent  # Assuming you have this class


class CarAgent(mesa.Agent):
    def __init__(self, model, spawn_position, target_parking_spot):
        """
        Initialize a CarAgent.

        Args:
            model (Model): The model instance that contains this agent.
            spawn_position (tuple): The initial position of the car agent.
        """
        super().__init__(model)
        self.active = True
        self.parking_spots = [
            coord for coord in model.parkings_coords if coord != spawn_position
        ]
        self.distance_travelled = 0
        self.target_parking_spot = random.choice(
            list(model.ParkingSpots.values())
        )  # Aqui rocha hizo un cochinero

    def check_semaphore(self, current_position):
        """
        Check the state of the semaphore at the current position.

        Args:
            current_position (tuple): The current position of the car agent.

        Returns:
            bool: True if the car can move, False otherwise.
        """
        agents_at_position = self.model.grid.get_cell_list_contents([current_position])
        semaphore_agent = None
        for agent in agents_at_position:
            if isinstance(agent, TrafficLightAgent):
                semaphore_agent = agent
        if semaphore_agent is None:
            return True
        else:
            if semaphore_agent.state == "red":
                print(f"Semaphore at {current_position} is red; agent cannot move.")
                return False
            elif semaphore_agent.state == "green":
                print(f"Semaphore at {current_position} is green; agent can move.")
                return True

    def check_agent(self, new_position):
        """
        Check if there is another car agent at the new position.

        Args:
            new_position (tuple): The new position to check.

        Returns:
            bool: True if the position is free, False otherwise.
        """
        agents_at_position = self.model.grid.get_cell_list_contents([new_position])
        car_agent = None
        for agent in agents_at_position:
            if isinstance(agent, CarAgent):
                car_agent = agent
        return car_agent is None

    def move(self):
        """
        Move the car agent to a new position based on allowed directions and semaphore state.
        """
        current_position = self.pos
        possible_current_directions = self.model.get_cell_directions(current_position)

        # Check for any available directions in this cell
        if not possible_current_directions:
            print(f"No directions available for agent at position {current_position}")
            return

        # Filter allowed directions and select one randomly
        possible_directions = [
            direction
            for direction, allowed in possible_current_directions.items()
            if allowed
        ]
        if not possible_directions:
            print(f"No movement options for agent at position {current_position}")
            return

        # Check if it can move according to the semaphore
        if not self.check_semaphore(current_position):
            return

        direction = random.choice(possible_directions)

        # Calculate the new position based on the chosen direction
        dx, dy = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}[
            direction
        ]

        new_position = (self.pos[0] + dx, self.pos[1] + dy)
        if not self.check_agent(new_position):
            return

        self.model.grid.move_agent(self, new_position)
        self.distance_travelled += 1  # Increment distance traveled
        self.pos = new_position  # Update the position

    def move_to_target(self):
        """
        Move the car agent towards the target parking spot.
        """
        while self.active:
            if self.pos in self.parking_spots and self.distance_travelled > 0:
                self.active = False
                break
            else:
                moved = self.move()
                if not moved:  # If the agent cannot move, stop the loop
                    break

    def step(self):
        """
        Advance the car agent by one step.
        """
        self.move_to_target()
