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
        print(f"Target parking spot: {self.target_parking_spot}")

    def check_semaphore(self, current_position):
        """Check the semaphore state at the current position."""
        from TrafficLightAgent import TrafficLightAgent

        agents_at_position = self.model.grid.get_cell_list_contents([current_position])
        semaphore_agent = None
        for agent in agents_at_position:
            if agent.__class__ == TrafficLightAgent:
                semaphore_agent = agent
        if semaphore_agent is None:
            return True
        else:
            if semaphore_agent.state == 1:
                return False
            elif semaphore_agent.state == 2:
                return True

    def check_agent(self, new_position):
        """Check if there is another car agent at the new position."""
        agents_at_position = self.model.grid.get_cell_list_contents([new_position])
        car_agent = None
        for agent in agents_at_position:
            if agent.__class__ == CarAgent:
                car_agent = agent
        return car_agent is None

    def move(self):
        """Move the agent to a new position."""
        current_position = self.pos
        possible_current_directions = self.model.get_cell_directions(current_position)

        if not possible_current_directions:
            return

        possible_directions = self.get_possible_directions(possible_current_directions)
        if not possible_directions:
            return

        if not self.check_semaphore(current_position):
            return

        direction = self.choose_direction(possible_directions)
        new_position = self.calculate_new_position(direction)

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
        """Get the list of possible directions the agent can move to."""
        return [
            direction
            for direction, allowed in possible_current_directions.items()
            if allowed
        ]

    def choose_direction(self, possible_directions):
        """Choose a direction to move to based on predefined weights."""
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
        """Calculate the new position based on the direction."""
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
        """Update the agent's position on the grid."""
        self.model.grid.move_agent(self, new_position)
        self.distance_travelled += 1
        self.pos = new_position

    def inteligent_move(self):
        """Move the agent intelligently towards the target parking spot."""
        current_position = self.pos

        # Define specific area checks
        area_checks = [
            ([(22, 10), (22, 11)], [(20, 15), (20, 18), (17, 21)], "up"),
            ([(22, 17), (22, 16)], [(17, 21)], "up"),
            (
                [(7, 11), (6, 11), (15, 11), (14, 11), (18, 1), (19, 1)],
                [(2, 14), (5, 17), (20, 4), (10, 19), (3, 21)],
                "up",
            ),
            ([(12, 22), (13, 22)], [(10, 19), (5, 17), (8, 15), (10, 12)], "down"),
            ([(6, 8), (7, 8), (7, 4), (7, 5)], [(9, 2)], "down"),
            ([(12, 17), (12, 18)], [(5, 17), (8, 15)], "down"),
        ]

        # Check if the agent is in a specific area and move accordingly
        for area, targets, direction in area_checks:
            if current_position in area and self.target_parking_spot in targets:
                new_position = self.calculate_new_position(direction)
                if not self.check_agent(new_position):
                    return
                self.update_position(new_position)
                return

        # Get possible moves and directions
        possible_moves = self.model.get_cell_directions(current_position)
        if not possible_moves:
            return

        possible_directions = self.get_possible_directions(possible_moves)
        if not possible_directions:
            return

        if not self.check_semaphore(current_position):
            return

        # Determine the best direction to move towards the target parking spot
        best_direction = self.find_best_direction(possible_directions)
        if best_direction is None:
            return

        new_position = self.calculate_new_position(best_direction)

        # Ensure the agent does not move to a parking spot that is not its target
        while (
            new_position in self.model.parkings_coords
            and new_position != self.target_parking_spot
        ):
            possible_directions.remove(best_direction)
            if not possible_directions:
                return
            best_direction = self.find_best_direction(possible_directions)
            if best_direction is None:
                return
            new_position = self.calculate_new_position(best_direction)

        if not self.check_agent(new_position):
            return

        self.update_position(new_position)

    def find_best_direction(self, possible_directions):
        """Find the best direction to move towards the target parking spot."""
        best_direction = None
        min_distance = float("inf")
        target_x, target_y = self.target_parking_spot

        for direction in possible_directions:
            new_position = self.calculate_new_position(direction)
            new_x, new_y = new_position
            distance = abs(target_x - new_x) + abs(
                target_y - new_y
            )  # Manhattan distance

            if distance < min_distance:
                min_distance = distance
                best_direction = direction

        return best_direction

    def move_to_target(self):
        """Move towards the target parking spot."""
        while self.active:
            if self.pos in self.parking_spots and self.distance_travelled > 0:
                self.active = False
                break
            else:
                moved = self.inteligent_move()
                if not moved:
                    break

    def step(self):
        """Execute one step of the agent."""
        self.move_to_target()
