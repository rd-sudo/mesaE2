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
        agents_at_position = self.model.grid.get_cell_list_contents([current_position])
        semaphore_agent = None
        for agent in agents_at_position:
            if agent.__class__ == TrafficLightAgent:
                semaphore_agent = agent
        if semaphore_agent is None:
            return True
        else:
            if semaphore_agent.state == 1:
                #print(f"Semaphore at {current_position} is red; agent cannot move.")
                return False
            elif semaphore_agent.state == 2:
                #print(f"Semaphore at {current_position} is green; agent can move.")
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
        current_position = self.pos
        possible_current_directions = self.model.get_cell_directions(current_position)
        
        if not possible_current_directions:
            return

        possible_directions = [direction for direction, allowed in possible_current_directions.items() if allowed]
        if not possible_directions:
            return

        if not self.check_semaphore(current_position):
            return 

        direction_map = {
            "up": (0, 1),
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0),
            "up_left": (-1, 1),
            "up_right": (1, 1),
            "down_left": (-1, -1),
            "down_right": (1, -1)
        }

        direction = random.choice(possible_directions)
        if direction not in direction_map:
            print(f"Invalid direction: {direction}")
            return

        dx, dy = direction_map[direction]
        new_position = (self.pos[0] + dx, self.pos[1] + dy)

        if not self.check_agent(new_position):
            return 

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





class TrafficLightAgent(mesa.Agent):
    def __init__(self, unique_id, state, model, monitored_positions):
        super().__init__(model)
        self.unique_id = unique_id
        self.state = state  
        self.time_counter = 0
        self.monitored_positions = monitored_positions
        self.neighbor_siblings = []  
        self.neighbor_opposites = []  

    def update_neighbors(self):
        """Actualiza las listas de semáforos hermanos y opuestos."""
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)

        self.neighbor_siblings = [
            agent for agent in neighbors if isinstance(agent, TrafficLightAgent) and agent.unique_id == self.unique_id
        ]
        self.neighbor_opposites = [
            agent for agent in neighbors if isinstance(agent, TrafficLightAgent) and agent.unique_id != self.unique_id
        ]

    def change_state(self, state):
        """Cambia el estado del semáforo automáticamente."""
        self.state = state

    def cars_in_monitored_area(self):
        """Revisa si hay autos en las posiciones monitoreadas."""

        in_area_cars = 0
        for pos in self.monitored_positions:
            agents = self.model.grid.get_cell_list_contents([pos])
            for agent in agents:
                if isinstance(agent, CarAgent):
                    in_area_cars += 1
        return in_area_cars




    def compare_traffic_with_neighbors(self):
        """Compara el tráfico en su área monitoreada con los vecinos y ajusta estados."""
        current_traffic = self.cars_in_monitored_area()
        
        # Imprimir información del agente actual
        #print(f"Traffic Light {self.unique_id} at {self.pos} with current state {self.state}")

        # Imprimir información de vecinos hermanos
        #print(f"  Sibling neighbors of Traffic Light {self.unique_id}:")
        for sibling in self.neighbor_siblings:
            sibling_traffic = sibling.cars_in_monitored_area()
            #print(f"    Sibling {sibling.unique_id} at {sibling.pos} with state {sibling.state} and traffic {sibling_traffic}")

        # Imprimir información de vecinos opuestos
        #print(f"  Opposite neighbors of Traffic Light {self.unique_id}:")
        for opposite in self.neighbor_opposites:
            opposite_traffic = opposite.cars_in_monitored_area()
            #print(f"    Opposite {opposite.unique_id} at {opposite.pos} with state {opposite.state} and traffic {opposite_traffic}")

        # Cambiar el estado basado en el tráfico
        if current_traffic == 0:
            self.change_state(3)
            for sibling in self.neighbor_siblings:
                sibling.change_state(3)
            return

        tempSelf = None  
        for opposite in self.neighbor_opposites:
            opposite_traffic = opposite.cars_in_monitored_area()
            if current_traffic > opposite_traffic:
                self.state = 2
                opposite.state = 1
                tempSelf = opposite  
                for sibling in self.neighbor_siblings:
                    sibling.state = self.state


        # Obtener vecinos de tempSelf
        if tempSelf:
            #print(f"TempSelf is set to Opposite Traffic Light {tempSelf.unique_id} at {tempSelf.pos} with state {tempSelf.state}")
            tempSelf_neighbors = self.model.grid.get_neighbors(tempSelf.pos, moore=True, include_center=False)
            tempSelf_traffic_lights = [
                agent for agent in tempSelf_neighbors if isinstance(agent, TrafficLightAgent)
            ]

            # Imprimir vecinos de tempSelf
            #print(f"  Neighbors of TempSelf (Traffic Light {tempSelf.unique_id}):")
            for neighbor in tempSelf_traffic_lights:
                neighbor_traffic = neighbor.cars_in_monitored_area()
                #print(f"    Neighbor {neighbor.unique_id} at {neighbor.pos} with state {neighbor.state} and traffic {neighbor_traffic}")
                if tempSelf.unique_id == neighbor.unique_id:
                    neighbor.state = tempSelf.state




    def step(self):
        """Actualizar el estado en cada paso."""
        self.time_counter += 1
        self.update_neighbors()  # Asegurarse de que las listas de vecinos estén actualizadas.
        self.compare_traffic_with_neighbors()
