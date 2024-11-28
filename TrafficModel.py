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
from TrafficLightAgent import TrafficLightAgent


class TrafficModel(mesa.Model):
    def __init__(
        self,
        width=24,
        height=24,
        num_agents=1,
        coords=None,
        buildings_coords=None,
        parking_coords=None,
        traffic_light_coords=None,
    ):
        super().__init__()
        # Initialize random number generator and step counter
        self.random = random.Random()
        self.steps = 0

        # Model parameters
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

        # Create a dictionary mapping each parking spot to a unique key starting from 1
        self.ParkingSpots = {i + 1: spot for i, spot in enumerate(parking_coords)}

        # Initialize grid layers
        self.initialize_layers()

        # Initialize the allowed directions for each cell
        self.initialize_directions(self.coords)

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

    # Initialize the grid layers for buildings, parking spots, and traffic monitoring
    def initialize_layers(self):
        buildingLayer = mesa.space.PropertyLayer(
            "building", self.width, self.height, np.int64(0), np.int64
        )
        parkingsLayer = mesa.space.PropertyLayer(
            "parking", self.width, self.height, np.int64(0), np.int64
        )
        trafficMonitoringLayer = mesa.space.PropertyLayer(
            "traffic_monitoring", self.width, self.height, np.int64(0), np.int64
        )

        self.set_building_cells(buildingLayer)
        self.set_parking_cells(parkingsLayer)
        self.set_traffic_monitoring_cells(trafficMonitoringLayer)

        self.grid = mesa.space.MultiGrid(
            self.width,
            self.height,
            True,
            (buildingLayer, parkingsLayer, trafficMonitoringLayer),
        )

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

    # Create car agents without a target parking spot
    def create_CarAgents_no_target(self):
        number_of_cars = 50
        all_coords = [(x, y) for x in range(self.width) for y in range(self.height)]
        available_coords = [
            coord
            for coord in all_coords
            if coord not in self.parkings_coords and coord not in self.buildings_coords
        ]

        if len(available_coords) < number_of_cars:
            raise ValueError("Not enough available coordinates to place all cars.")

        for _ in range(number_of_cars):
            spawn_position = random.choice(available_coords)
            available_coords.remove(spawn_position)
            agent = CarAgent(self, spawn_position, None)
            self.grid.place_agent(agent, spawn_position)

    # Create car agents and place them on the grid
    def create_CarAgents(self):
        spawn_spots = list(self.ParkingSpots.values())  # Copy of available spawn spots
        target_spots = list(
            self.ParkingSpots.values()
        )  # Copy of available target spots

        for i in range(self.num_agents):
            # Check if there are available spawn spots
            if not spawn_spots:
                print("No available spawn spots left")
                break

            # Select a unique spawn spot
            Spawn = random.choice(spawn_spots)
            spawn_spots.remove(Spawn)  # Remove the spawn spot to avoid reuse

            # Filter target spots, excluding the current spawn spot
            possible_target_spots = [spot for spot in target_spots if spot != Spawn]

            # Check if there are available target spots
            if not possible_target_spots:
                print("No available target spots left")
                break

            # Select a unique target spot
            target_parking_spot = random.choice(possible_target_spots)
            target_spots.remove(
                target_parking_spot
            )  # Remove the target spot to avoid reuse

            print(f"Spawn: {Spawn}, Target: {target_parking_spot}")

            # Create the agent with the assigned spots
            agent = CarAgent(self, Spawn, target_parking_spot)

            # Place the agent on the grid at its spawn position
            self.grid.place_agent(agent, Spawn)

    # Place traffic light agents on the grid
    def place_TrafficLight_agents(self):
        for idx, traffic_light_info in enumerate(self.traffic_light_coords):
            traffic_light_id = idx  # Unique ID for each traffic light
            positions = traffic_light_info[
                :2
            ]  # Assuming the positions are the first two values
            initial_state = traffic_light_info[
                2
            ]  # The initial state is the third value
            monitored_coords = traffic_light_info[3]

            # Create the traffic light agent for each position
            for pos in positions:
                sema_agent = TrafficLightAgent(
                    traffic_light_id,
                    initial_state,
                    self,
                    monitored_positions=monitored_coords,
                )

                # Place the agent on the grid
                self.grid.place_agent(sema_agent, pos)

    # Fetch the direction info for a specific cell
    def get_cell_directions(self, pos):
        return self.directions.get(pos, None)

    # Create a global map of the current state of the simulation
    def get_global_map(self):
        car_agents = []
        traffic_lights = {}

        self.global_map = {"Cars": [], "Traffic_Lights": {}}

        for contents, (x, y) in self.grid.coord_iter():
            for agent in contents:
                if isinstance(agent, CarAgent):
                    car_agents.append(agent)
                elif isinstance(agent, TrafficLightAgent):
                    traffic_lights[f"sema_{agent.unique_id}"] = agent.state

        # Sort car agents by unique_id
        car_agents.sort(key=lambda agent: agent.unique_id)

        # Add sorted car agents to the global map
        for agent in car_agents:
            self.global_map["Cars"].append({"x": agent.pos[0], "y": agent.pos[1]})

        # Add traffic lights to the global map
        self.global_map["Traffic_Lights"] = traffic_lights
        return self.global_map

    # Set the value of cells to indicate buildings
    def set_building_cells(self, buildingLayer):
        for coord in self.buildings_coords:
            buildingLayer.set_cell(coord, 1)

    # Set the value of cells to indicate parking spots
    def set_parking_cells(self, parkingsLayer):
        for coord in self.parkings_coords:
            parkingsLayer.set_cell(coord, 1)

    # Set the value of cells to indicate traffic monitoring spots
    def set_traffic_monitoring_cells(self, trafficMonitoringLayer):
        all_monitored_coords = []
        for traffic_light in self.traffic_light_coords:
            monitored_coords = traffic_light[-1]
            all_monitored_coords.extend(monitored_coords)

        for coord in all_monitored_coords:
            trafficMonitoringLayer.set_cell(coord, 1)

    # Check if there is traffic in a given area
    def traffic_in_area(self, area):
        count = 0
        for pos in area:
            for agent in self.grid.get_cell_list_contents(pos):
                if isinstance(agent, CarAgent):
                    count += 1
        return count > 10

    # Modify street directions based on traffic
    def modify_street_with_traffic(self):
        for key, value in self.coords["monitoring_coords"].items():
            pos = value["pos"]
            area = value["area"]
            direction = value["direction"]

            if self.traffic_in_area(area):
                self.directions[pos][direction] = False
            else:
                self.directions[pos][direction] = True

    # Execute one step of the model, shuffle agents, and collect data
    def step(self):
        # Shuffle and execute the step method for all agents
        self.agents.shuffle_do("step")
        # Collect data for the current step
        self.datacollector.collect(self)
        # Create a global map of the current state
        self.get_global_map()
