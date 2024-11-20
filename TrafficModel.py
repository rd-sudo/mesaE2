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
    ):
        """
        Initialize the TrafficModel.

        Args:
            width (int): Width of the grid.
            height (int): Height of the grid.
            num_agents (int): Number of car agents.
            left_coords (list): Coordinates with left direction.
            right_coords (list): Coordinates with right direction.
            up_coords (list): Coordinates with up direction.
            down_coords (list): Coordinates with down direction.
            buildings_coords (list): Coordinates of buildings.
            parking_coords (list): Coordinates of parking spots.
            traffic_light_coords (list): Coordinates and states of traffic lights.
        """
        super().__init__()
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.parkings_coords = parking_coords
        self.traffic_light_coords = traffic_light_coords
        self.steps = 0
        self.random = random.Random()
        self.directions = {}
        self.global_map = {}
        self.ParkingSpots = {i + 1: spot for i, spot in enumerate(parking_coords)}

        # Initialize the grid with building and parking layers
        buildingLayer = mesa.space.PropertyLayer(
            "building", width, height, np.int64(0), np.int64
        )
        parkingsLayer = mesa.space.PropertyLayer(
            "parking", width, height, np.int64(0), np.int64
        )
        self.set_building_cells(buildings_coords, buildingLayer)
        self.set_parking_cells(parking_coords, parkingsLayer)
        self.grid = mesa.space.MultiGrid(
            width, height, True, (buildingLayer, parkingsLayer)
        )

        # Create agents and place them on the grid
        self.create_agents()

        # Initialize directions for each cell
        self.initialize_directions(left_coords, right_coords, up_coords, down_coords)

        # Place traffic light agents on the grid
        self.place_traffic_light_agents()

        # Initialize the DataCollector
        self.datacollector = mesa.DataCollector(
            model_reporters={},
            agent_reporters={
                "TargetParkingSpot": lambda agent: (
                    agent.target_parking_spot if isinstance(agent, CarAgent) else None
                )
            },
        )
        self.datacollector.collect(self)

    def create_agents(self):
        """Create car agents and place them on the grid."""
        used_parking_spots = set()
        for i in range(self.num_agents):
            available_spawn_spots = [
                spot
                for spot in self.ParkingSpots.values()
                if spot not in used_parking_spots
            ]
            if not available_spawn_spots:
                print("No available spots for spawn")
                break
            spawn = random.choice(available_spawn_spots)
            used_parking_spots.add(spawn)

            available_target_spots = [
                spot
                for spot in self.ParkingSpots.values()
                if spot != spawn and spot not in used_parking_spots
            ]
            if not available_target_spots:
                print("No available spots for target parking")
                break
            target_parking_spot = random.choice(available_target_spots)
            used_parking_spots.add(
                target_parking_spot
            )  # Aqui rocha hizo un cochinero target_parking_spot##########

            print(f"Spawn: ({spawn}), Target: ({target_parking_spot})")
            agent = CarAgent(self, spawn, target_parking_spot)
            self.grid.place_agent(agent, spawn)

    def initialize_directions(self, left_coords, right_coords, up_coords, down_coords):
        """Initialize allowed directions for each cell."""
        for x in range(self.width):
            for y in range(self.height):
                self.directions[(x, y)] = {
                    "left": False,
                    "right": False,
                    "up": False,
                    "down": False,
                }

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

    def place_traffic_light_agents(self):
        """Place traffic light agents on the grid."""
        for idx, traffic_light_info in enumerate(self.traffic_light_coords):
            traffic_light_id = f"sema_{idx}"
            positions = traffic_light_info[:2]
            initial_state = traffic_light_info[2]
            for pos in positions:
                sema_agent = TrafficLightAgent(traffic_light_id, initial_state, self)
                self.grid.place_agent(sema_agent, pos)

    def set_building_cells(self, buildings_coords, buildingLayer):
        """Set building cells on the grid."""
        for coord in buildings_coords:
            buildingLayer.set_cell(coord, 1)

    def set_parking_cells(self, parking_coords, parkingsLayer):
        """Set parking cells on the grid."""
        for coord in parking_coords:
            parkingsLayer.set_cell(coord, 1)

    def get_cell_directions(self, pos):
        """Fetch the direction info for a specific cell."""
        return self.directions.get(pos, None)

    def step(self):
        """Advance the model by one step."""
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
        self.create_global_map()

    def create_global_map(self):
        """Create a global map of the current state of the model."""
        self.global_map = {"Cars": [], "Traffic_Lights": {}}
        car_agents = []
        trafficLight = {}

        for contents, (x, y) in self.grid.coord_iter():
            for agent in contents:
                if isinstance(agent, CarAgent):
                    car_agents.append(agent)
                elif isinstance(agent, TrafficLightAgent):
                    trafficLight[agent.unique_id] = agent.state == "green"

        car_agents.sort(key=lambda agent: agent.unique_id)
        for agent in car_agents:
            self.global_map["Cars"].append(agent.pos)
        self.global_map["Traffic_Lights"] = trafficLight
        # print(self.global_map)
        return self.global_map
