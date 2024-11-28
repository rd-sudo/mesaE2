import mesa
import numpy as np
import random


class CarAgent(mesa.Agent):
    def __init__(self, model, spawn_position, target_parking_spot=None):
        super().__init__(model)
        self.active = True
        self.parking_spots = [
            coord for coord in model.parkings_coords if coord != spawn_position
        ]
        self.distance_travelled = 0
        self.target_parking_spot = target_parking_spot

    def check_semaphore(
        self, current_position
    ):  # for future implementation, check if the agent is a car
        from TrafficLightAgent import (
            TrafficLightAgent,
        )  # importing here to avoid circular import

        agents_at_position = self.model.grid.get_cell_list_contents([current_position])
        semaphore_agent = None
        for agent in agents_at_position:
            if agent.__class__ == TrafficLightAgent:
                semaphore_agent = agent
        if semaphore_agent is None:
            return True
        else:
            if semaphore_agent.state == 1:
                print(f"Semaphore at {current_position} is red; agent cannot move.")
                return False
            elif semaphore_agent.state == 2:
                print(f"Semaphore at {current_position} is green; agent can move.")
                return True

    def check_agent(self, new_position):
        agents_at_position = self.model.grid.get_cell_list_contents([new_position])
        car_agent = None
        for agent in agents_at_position:
            if agent.__class__ == CarAgent:
                car_agent = agent
        if car_agent is None:
            return True
        else:
            return False

    def move(self):
        # Get current position and allowed directions
        current_position = self.pos
        possible_current_directions = self.model.get_cell_directions(current_position)

        # Check for any available directions in this cell
        if not possible_current_directions:
            print(f"No directions available for agent at position {current_position}")
            return

        # Filter allowed directions and select one randomly
        possible_directions = self.get_possible_directions(possible_current_directions)
        if not possible_directions:
            print(f"No movement options for agent at position {current_position}")
            return

        # Checks if it can move acccording to the sempahore
        if not self.check_semaphore(current_position):
            return

        direction = self.choose_direction(possible_directions)
        new_position = self.calculate_new_position(direction)

        # Logic to not allow the agent to move to a parking spot that is not its target
        while (
            new_position in self.model.parkings_coords
            and new_position != self.target_parking_spot
        ):
            direction = self.choose_direction(possible_directions)
            new_position = self.calculate_new_position(direction)

        if not self.check_agent(new_position):
            return

        self.update_position(new_position)

    def get_possible_directions(self, possible_current_directions):
        return [
            direction
            for direction, allowed in possible_current_directions.items()
            if allowed
        ]

    def choose_direction(self, possible_directions):
        direction_weights = {
            "up": 1,
            "down": 1,
            "left": 1,
            "right": 1,
            "down_left": 0.1,
            "down_right": 0.1,
            "up_left": 0.1,
            "up_right": 0.1,
        }
        weights = [direction_weights[direction] for direction in possible_directions]
        return random.choices(possible_directions, weights=weights, k=1)[0]

    def calculate_new_position(self, direction):
        direction_map = {
            "up": (0, 1),
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0),
            "down_left": (-1, -1),
            "down_right": (1, -1),
            "up_left": (-1, 1),
            "up_right": (1, 1),
        }
        dx, dy = direction_map[direction]
        return (self.pos[0] + dx, self.pos[1] + dy)

    def update_position(self, new_position):
        self.model.grid.move_agent(self, new_position)
        self.distance_travelled += 1
        self.pos = new_position

    def move_to_target(self):
        # Moverse hasta alcanzar el destino
        while self.active:
            if self.pos in self.parking_spots and self.distance_travelled > 0:
                self.active = False
                break
            else:
                moved = self.move()
                if not moved:  # Si no puede moverse, detener el bucle
                    break

    def step(self):
        self.move_to_target()
