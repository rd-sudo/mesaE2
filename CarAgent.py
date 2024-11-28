import mesa
import numpy as np
import random



class CarAgent(mesa.Agent):
    def __init__(self, model, spawn_position, target_parking_spot):
        super().__init__(model)
        self.active = True
        self.parking_spots = [coord for coord in model.parkings_coords if coord != spawn_position]
        self.distance_travelled = 0
        self.target_parking_spot = random.choice(list(model.ParkingSpots.values()))

    def check_semaphore(self, current_position): #for future implementation, check if the agent is a car
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
        possible_directions = [direction for direction, allowed in possible_current_directions.items() if allowed]
        if not possible_directions:
            print(f"No movement options for agent at position {current_position}")
            return

        # Checks if it can move acccording to the sempahore
        if not self.check_semaphore(current_position):
            return 

        direction = random.choice(possible_directions)

        # Calculate the new position based on the chosen direction
        dx, dy = {
            "up": (0, 1),
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0)
        }[direction]

        new_position = (self.pos[0] + dx, self.pos[1] + dy)
        if not self.check_agent(new_position):
            return 
        
        self.model.grid.move_agent(self, new_position)
        self.distance_travelled += 1  # Increment distance traveled
        self.pos = new_position       # Update the position
            
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