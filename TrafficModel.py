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
        # ATTRIBUTES OF THE MODEL----------------------------------------------------------------------------------
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.coords = coords
        self.buildings_coords = buildings_coords
        self.parkings_coords = parking_coords
        self.traffic_light_coords = traffic_light_coords

        # Initialize random generator and step counter
        self.random = random.Random()
        self.steps = 0

        # Initialize direction dictionary and global maps
        self.directions = {}
        self.global_map_cars = {}
        self.global_map_traffic_lights = {}
        self.traffic_light_groups = {}

        # Create a dictionary mapping each parking spot to a unique key
        self.ParkingSpots = {i + 1: spot for i, spot in enumerate(self.parkings_coords)}

        # Initialize grid layers
        self.initialize_layers()

        # CREATION OF AGENTS IN THE GRID---------------------------------------
        # Initialize agents and their positions
        self.initialize_agents()

        # Initialize data collector
        self.datacollector = mesa.DataCollector(model_reporters={}, agent_reporters={})
        self.datacollector.collect(self)

    # LAYERS OF THE GRID---------------------------------------
    def initialize_layers(self):
        """Initialize the grid layers for buildings, parking spots, and traffic monitoring."""
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
        """I am checking if the traffic lights are checking the right amount of cars in their monitored area
        list_of_cords_of_traffic_lights = [(2, 4),(0, 6)]
        for cord in list_of_cords_of_traffic_lights:
            for agent in self.grid.get_cell_list_contents(cord):
                if isinstance(agent, TrafficLightAgent):
                    print(f"Agent:{agent.traffic_light_id} Found: {agent.cars_in_monitored_area()} in his area.")
        """

    # INITIALIZER METHODS----------------------------------------------------------------------------------
    def initialize_agents(self):
        """Initialize the agents in the grid."""
        self.initialize_directions(self.coords)
        self.create_traffic_light_groups()
        self.create_CarAgents()
        self.create_CarAgents_no_target()
        self.place_TrafficLight_agents()

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

    def create_CarAgents_no_target(self):
        """Create car agents without a target parking spot."""
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

    # Create agents and place them on the grid
    def create_CarAgents(self):
        """Create car agents and place them on the grid."""
        used_parking_spots = set()

        for _ in range(self.num_agents):
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
            used_parking_spots.add(target_parking_spot)

            print(f"Spawn: ({spawn}), Target: ({target_parking_spot})")

            agent = CarAgent(self, spawn, target_parking_spot)
            self.grid.place_agent(agent, spawn)

    # TRAFFIC LIGHT METHODS----------------------------------------------------------------------------------
    def place_TrafficLight_agents(self):
        for traffic_light_id, traffic_light_info in self.traffic_light_coords.items():
            positions = traffic_light_info["position"]
            initial_state = traffic_light_info["state"]
            group = traffic_light_info["group"]
            monitored_coords = traffic_light_info["monitored_coords"]

            # Create separate agents with the same id and place them in the corresponding positions
            for pos in positions:
                sema_agent = TrafficLightAgent(
                    traffic_light_id=traffic_light_id,
                    state=initial_state,
                    model=self,
                    group=group,
                    position=positions,
                    monitored_positions=monitored_coords,
                )  # Assign the same id
                self.grid.place_agent(sema_agent, pos)

    def create_traffic_light_groups(self):
        """Create a map of traffic light groups."""
        for traffic_light_id, traffic_light_info in self.traffic_light_coords.items():
            group = traffic_light_info["group"]
            if group not in self.traffic_light_groups:
                self.traffic_light_groups[group] = []
            self.traffic_light_groups[group].append(traffic_light_id)

    # GETTER METHODS----------------------------------------------------------------------------------
    def get_cell_directions(self, pos):
        """Fetch the direction info for a specific cell."""
        return self.directions.get(pos, None)

    # Create a global map of the current state of the simulation
    def get_global_map(self):
        """Create a global map of the current state of the simulation."""
        self.global_map_cars = {"Cars": []}
        self.global_map_traffic_lights = {"Traffic_Lights": {}}

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
            self.global_map_cars["Cars"].append(agent.pos)

        self.global_map_traffic_lights["Traffic_Lights"] = trafficLight

        return self.global_map_cars, self.global_map_traffic_lights

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
        for traffic_light in self.traffic_light_coords.values():
            all_monitored_coords.extend(traffic_light["monitored_coords"])
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
