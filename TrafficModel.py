"""
City Simulation Model
=============================================================
A Mesa implementation of a city simulation model, where the cars
move randomly around the city and go to the parking spots in there.
"""

import mesa
import time
import seaborn as sns
import random
import numpy as np
import pandas as pd

from agents import CarAgent, TrafficLightAgent

from mapBuild.leftCoords import left_coords
from mapBuild.rightCoords import right_coords
from mapBuild.upCoords import up_coords
from mapBuild.downCoords import down_coords
from mapBuild.downLeftCoords import down_left_coords
from mapBuild.downRightCoords import down_right_coords
from mapBuild.upLeftCoords import up_left_coords
from mapBuild.upRightCoords import up_right_coords

from mapBuild.monitoring_coords import monitoring_coords


# Storing the coordinates in a dictionary
coords = {
    "left_coords": left_coords,
    "right_coords": right_coords,
    "up_coords": up_coords,
    "down_coords": down_coords,
    "down_left_coords": down_left_coords,
    "down_right_coords": down_right_coords,
    "up_left_coords": up_left_coords,
    "up_right_coords": up_right_coords,
    "monitoring_coords": monitoring_coords,
}


class TrafficModel(mesa.Model):
    def __init__(
        self,
        width=24,
        height=24,
        num_agents=1,
        coords = coords,
        buildings_coords=None,
        parking_coords=None,
        traffic_light_coords=None,
    ):
        
        
        
        
        super().__init__()
        #ATTRIBUTES OF THE MODEL----------------------------------------------------------------------------------
        self.random = random.Random()
        self.steps = 0

        #Parameters
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.coords = coords
        self.buildings_coords = buildings_coords
        self.parkings_coords = parking_coords
        self.traffic_light_coords = traffic_light_coords

        # Dictionary to store directions for each cell
        self.directions = {}

        # Global map to store the positions of all agents at each step
        self.global_map = {}
        
        
        #Create a dictionary mapping each parking spot to a unique key starting from 1
        self.ParkingSpots = {i + 1: spot for i, spot in enumerate(parking_coords)}
        
        # Initialize grid layers
        self.initialize_layers()
    
        #CREATION OF AGENTS IN THE GRID---------------------------------------    
        # Initialize the allowed directions for each cell
        self.initialize_directions(self.coords)

        # Create the CarAgents and place them on the grid
        self.create_CarAgents()
        #self.create_CarAgents_no_target()

        # Place the traffic lights on the grid
        self.place_TrafficLight_agents()

        # Initialize the DataCollector
        self.datacollector = mesa.DataCollector(
            model_reporters={},
            agent_reporters={
                "TargetParkingSpot": lambda agent: (
                    agent.target_parking_spot if isinstance(agent, CarAgent) else None
                )
            },
        )

        # Collect initial data
        self.datacollector.collect(self)

    #LAYERS OF THE GRID--------------------------------------
    def initialize_layers(self):
        """Initialize the grid layers for buildings, parking spots, and traffic monitoring."""
        buildingLayer = mesa.space.PropertyLayer("building", self.width, self.height, np.int64(0), np.int64)
        parkingsLayer = mesa.space.PropertyLayer("parking", self.width, self.height, np.int64(0), np.int64)
        trafficMonitoringLayer = mesa.space.PropertyLayer("traffic_monitoring", self.width, self.height, np.int64(0), np.int64)

        self.set_building_cells(buildingLayer)
        self.set_parking_cells(parkingsLayer)
        self.set_traffic_monitoring_cells(trafficMonitoringLayer)

        self.grid = mesa.space.MultiGrid(self.width, self.height, True, (buildingLayer, parkingsLayer, trafficMonitoringLayer))
    #INITIALIZER METHODS----------------------------------------------------------------------------------
    # Initialize allowed directions for each cell in the grid
    def initialize_directions(self, coords):
        for x in range(self.width):
            for y in range(self.height):
                self.directions[(x, y)] = {
                    "left": False,
                    "right": False,
                    "up": False,
                    "down": False,
                    "down_left": False,
                    "down_right": False,
                    "up_left": False,
                    "up_right": False,
                    "traffic_left": False,
                    "traffic_right": False,
                    "traffic_up": False,
                    "traffic_down": False,
                }

        # Set specific directions for each list
        for coord in coords["left_coords"]:
            if coord in self.directions:
                self.directions[coord]["left"] = True

        for coord in coords["right_coords"]:
            if coord in self.directions:
                self.directions[coord]["right"] = True

        for coord in coords["up_coords"]:
            if coord in self.directions:
                self.directions[coord]["up"] = True

        for coord in coords["down_coords"]:
            if coord in self.directions:
                self.directions[coord]["down"] = True

        for coord in coords["down_left_coords"]:
            if coord in self.directions:
                self.directions[coord]["down_left"] = True

        for coord in coords["down_right_coords"]:
            if coord in self.directions:
                self.directions[coord]["down_right"] = True

        for coord in coords["up_left_coords"]:
            if coord in self.directions:
                self.directions[coord]["up_left"] = True

        for coord in coords["up_right_coords"]:
            if coord in self.directions:
                self.directions[coord]["up_right"] = True

     # Create agents and place them on the grid
    def create_CarAgents(self):
        # Crear listas separadas para manejar spawn y target
        spawn_spots = list(self.ParkingSpots.values())  # Copia de espacios de spawn disponibles
        target_spots = list(self.ParkingSpots.values())  # Copia de espacios para objetivos

        for i in range(self.num_agents):
            # Verificar si hay lugares disponibles para spawn
            if not spawn_spots:
                print("No available spawn spots left")
                break

            # Seleccionar un espacio de spawn único
            Spawn = random.choice(spawn_spots)
            spawn_spots.remove(Spawn)  # Remover el espacio de spawn para evitar reutilización

            # Filtrar espacios para el target, excluyendo el spawn actual
            possible_target_spots = [spot for spot in target_spots if spot != Spawn]

            # Verificar si hay lugares disponibles para el target
            if not possible_target_spots:
                print("No available target spots left")
                break

            # Seleccionar un espacio objetivo único
            target_parking_spot = random.choice(possible_target_spots)
            target_spots.remove(target_parking_spot)  # Remover el espacio de target para evitar reutilización

            print(f"Spawn: {Spawn}, Target: {target_parking_spot}")

            # Crear el agente con los espacios asignados
            agent = CarAgent(self, Spawn, target_parking_spot)

            # Colocar el agente en el grid en su posición de spawn
            self.grid.place_agent(agent, Spawn)

    # Place traffic light agents on the grid
# Place traffic light agents on the grid
    def place_TrafficLight_agents(self):
        for idx, traffic_light_info in enumerate(self.traffic_light_coords):
            traffic_light_id = idx # Unique ID for each traffic light
            positions = traffic_light_info[:2]  # Assuming the positions are the first two values
            initial_state = traffic_light_info[2]  # The initial state is the third value
            monitored_coords = traffic_light_info[3]
            #print(f"Monitored positions: {monitored_coords}")

            # Create the traffic light agent for each position
            for pos in positions:
                # Ensure the position is passed when creating the agent
                sema_agent = TrafficLightAgent(
                    traffic_light_id, initial_state, self,monitored_positions=monitored_coords

                )  # Assign the ID, state, model, and position

                # Place the agent on the grid
                self.grid.place_agent(sema_agent, pos)

                # Print information about the placed agent
                #print(f"Placed TrafficLightAgent: ID={sema_agent.unique_id}, State={sema_agent.state}, Position={sema_agent.pos}")
                
        
                
                
    #GETTER METHODS----------------------------------------------------------------------------------
    # Fetch the direction info for a specific cell
    def get_cell_directions(self, pos):    
        return self.directions.get(pos, None)

    # Create a global map of the current state of the simulation
# Create a global map of the current state of the simulation
    def get_global_map(self):
        """
        Generate a global map of the current state of the simulation in the specified JSON format.
        """
        # Inicializar el mapa global
        self.global_map = {
            "Cars": [],
            "Traffic_Lights": {}
        }

        # Recopilar agentes
        for contents, (x, y) in self.grid.coord_iter():
            for agent in contents:
                if isinstance(agent, CarAgent):
                    # Agregar las coordenadas del agente CarAgent al formato deseado
                    self.global_map["Cars"].append({"x": x, "y": y})
                elif isinstance(agent, TrafficLightAgent):
                    # Agregar datos del semáforo al formato deseado
                    self.global_map["Traffic_Lights"][f"sema_{agent.unique_id}"] = agent.state

        # Debug: Imprimir el mapa global
        print(self.global_map)

        # Devolver el mapa global en el formato solicitado
        return self.global_map

        
    # LAYER METHODS----------------------------------------------------------------------------------
    def set_building_cells(self, buildingLayer):
        """Set the value of cells to indicate buildings."""
        for coord in self.buildings_coords:
            buildingLayer.set_cell(coord, 1)

    def set_parking_cells(self, parkingsLayer):
        """Set the value of cells to indicate parking spots."""
        for coord in self.parkings_coords:
            parkingsLayer.set_cell(coord, 1)

    def set_traffic_monitoring_cells(self, trafficMonitoringLayer):
        """Set the value of cells to indicate traffic monitoring spots."""
        all_monitored_coords = []
        for traffic_light in self.traffic_light_coords:
            # Access monitored coordinates assuming they are the last element in each list
            monitored_coords = traffic_light[-1]
            all_monitored_coords.extend(monitored_coords)

        for coord in all_monitored_coords:
            trafficMonitoringLayer.set_cell(coord, 1)


    # STEP METHOD----------------------------------------------------------------------------------
    # Execute one step of the model, shuffle agents, and collect data
    def step(self):
        # Shuffle and execute the step method for all agents
        self.agents.shuffle_do("step")
        # Collect data for the current step
        self.datacollector.collect(self)
        # Create a global map of the current state
        self.get_global_map()



