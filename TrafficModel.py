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
from CarAgent import CarAgent
from TrafficLightAgent import TrafficLightAgent  # Assuming you have this class


class TrafficModel(mesa.Model):
    def __init__(
        self,
        width=24,
        height=24,
        num_agents=1,
        left_coords=None,
        right_coords=None,
        up_coords=None,
        down_coords=None,
        buildings_coords=None,
        parking_coords=None,
        traffic_light_coords=None,
        seed = None
    ):
        super().__init__()
        # ATTRIBUTES OF THE MODEL----------------------------------------------------------------------------------
        self.random = random.Random()
        self.steps = 0

        # Parameters
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.parkings_coords = parking_coords
        self.traffic_light_coords = traffic_light_coords

        # Dictionary to store directions for each cell
        self.directions = {}

        # Global map to store the positions of all agents at each step
        self.global_map = {}

        # Create a dictionary mapping each parking spot to a unique key starting from 1
        self.ParkingSpots = {i + 1: spot for i, spot in enumerate(parking_coords)}

        # LAYERS OF THE GRID---------------------------------------
        # Layer for buildings
        buildingLayer = mesa.space.PropertyLayer(
            "building", width, height, np.float64(0)
        )
        # layer for parking spots
        parkingsLayer = mesa.space.PropertyLayer(
            "parking", width, height, np.float64(0)
        )

        # Set the to layer to its corresponding cell
        self.set_building_cells(buildings_coords, buildingLayer)
        self.set_parking_cells(parking_coords, parkingsLayer)

        # Create a MultiGrid object the two layers
        self.grid = mesa.space.MultiGrid(
            width, height, True, (buildingLayer, parkingsLayer)
        )

        # CREATION OF AGENTS IN THE GRID---------------------------------------
        # Initialize the allowed directions for each cell
        self.initialize_directions(left_coords, right_coords, up_coords, down_coords)

        # Create the CarAgents and place them on the grid
        self.create_CarAgents()

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

    # INITIALIZER METHODS----------------------------------------------------------------------------------
    # Initialize allowed directions for each cell in the grid
    def initialize_directions(self, left_coords, right_coords, up_coords, down_coords):
        for x in range(self.width):
            for y in range(self.height):
                self.directions[(x, y)] = {
                    "left": False,
                    "right": False,
                    "up": False,
                    "down": False,
                }

        # Set specific directions for each list
        for coord in left_coords:
            if coord in self.directions:
                self.directions[coord]["left"] = True

        for coord in right_coords:
            if coord in self.directions:
                self.directions[coord]["right"] = True

        for coord in up_coords:
            if coord in self.directions:
                self.directions[coord]["up"] = True

        for coord in down_coords:
            if coord in self.directions:
                self.directions[coord]["down"] = True

    # Create agents and place them on the grid
    def create_CarAgents(self):
        used_parking_spots = set()

        for i in range(self.num_agents):
            available_spawn_spots = [
                spot
                for spot in self.ParkingSpots.values()
                if spot not in used_parking_spots
            ]

            if available_spawn_spots:
                Spawn = random.choice(available_spawn_spots)
            else:
                # If no available spots for spawning, take some action (e.g., break or similar)
                print("No available spots for spawn")
                break

            used_parking_spots.add(Spawn)

            # Create a list of available spots for the target parking (excluding the spawn spot and used spots)
            available_target_spots = [
                spot
                for spot in self.ParkingSpots.values()
                if spot != Spawn and spot not in used_parking_spots
            ]

            if available_target_spots:
                target_parking_spot = random.choice(available_target_spots)
            else:
                # If no available spots for target parking, take some action (e.g., break or continue)
                print("No available spots for target parking")
                break  # or continue with some other action.

            # Mark the target spot as used
            used_parking_spots.add(target_parking_spot)

            print(f"Spawn: ({Spawn}), Target: ({target_parking_spot})")

            agent = CarAgent(self, Spawn, target_parking_spot)  # Pass the coordinates

            # Place the agent in the 'Spawn' cell using the correct coordinates
            self.grid.place_agent(agent, Spawn)

    # Place traffic light agents on the grid
    def place_TrafficLight_agents(self):
        for idx, traffic_light_info in enumerate(self.traffic_light_coords):
            traffic_light_id = f"sema_{idx}"  # Unique ID for each traffic light
            positions = traffic_light_info[:2]
            initial_state = traffic_light_info[2]

            # Create two separate agents with the same id and place them in the corresponding positions
            for pos in positions:
                sema_agent = TrafficLightAgent(
                    traffic_light_id, initial_state, self
                )  # Assign the same id
                self.grid.place_agent(sema_agent, pos)

    # GETTER METHODS----------------------------------------------------------------------------------
    # Fetch the direction info for a specific cell
    def get_cell_directions(self, pos):
        return self.directions.get(pos, None)

    # Create a global map of the current state of the simulation
    def get_global_map(self):
        # Add the current step and agents' positions to the global_map
        self.global_map = {"Cars": [], "Traffic_Lights": {}}

        # Collect all CarAgents and TrafficLightAgents and sort them by unique_id
        car_agents = []
        trafficLight = {}

        for contents, (x, y) in self.grid.coord_iter():
            for agent in contents:
                if isinstance(agent, CarAgent):
                    car_agents.append(agent)
                elif isinstance(agent, TrafficLightAgent):
                    trafficLight[agent.unique_id] = agent.state == "green"

        car_agents.sort(key=lambda agent: agent.unique_id)

        # Append the positions of the sorted CarAgents to the global_map
        for agent in car_agents:
            self.global_map["Cars"].append({"x": agent.pos[0], "y": agent.pos[1]})

        # Append the traffic light states to the global_map
        self.global_map["Traffic_Lights"] = trafficLight
        return self.global_map

    # LAYER METHODS----------------------------------------------------------------------------------
    # Set the value of cells to indicate buildings
    def set_building_cells(self, buildings_coords, buildingLayer):
        for coord in buildings_coords:
            buildingLayer.set_cell(coord, 1)

    # Set the value of cells to indicate parking spots
    def set_parking_cells(self, parking_coords, parkingsLayer):

        for coord in parking_coords:
            parkingsLayer.set_cell(coord, 1)

    # STEP METHOD----------------------------------------------------------------------------------
    # Execute one step of the model, shuffle agents, and collect data
    def step(self):
        # Shuffle and execute the step method for all agents
        self.agents.shuffle_do("step")
        # Collect data for the current step
        self.datacollector.collect(self)
        # Create a global map of the current state
        self.get_global_map()
