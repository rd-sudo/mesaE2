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
        
        
        
        
        super().__init__()
        #ATTRIBUTES OF THE MODEL----------------------------------------------------------------------------------
        self.random = random.Random()
        self.steps = 0

        #Parameters
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.parkings_coords = parking_coords
        self.traffic_light_coords = traffic_light_coords

        # Dictionary to store directions for each cell
        self.directions = {}

        # Global map to store the positions of all agents at each step
        self.global_map = {}
        self.buildings_coords = buildings_coords
        
        #Create a dictionary mapping each parking spot to a unique key starting from 1
        self.ParkingSpots = {i + 1: spot for i, spot in enumerate(parking_coords)}
        
        
        
        #LAYERS OF THE GRID---------------------------------------
        #Layer for buildings
        buildingLayer = mesa.space.PropertyLayer(
            "building", width, height, np.int64(0), np.int64
        )
        #layer for parking spots
        parkingsLayer = mesa.space.PropertyLayer(
            "parking", width, height, np.int64(0), np.int64
        )
        trafficMonitoringLayer = mesa.space.PropertyLayer("traffic_monitoring", self.width, self.height, np.int64(0), np.int64)
        self.set_traffic_monitoring_cells(trafficMonitoringLayer)

        # Set the to layer to its corresponding cell
        self.set_building_cells(buildings_coords, buildingLayer)
        self.set_parking_cells(parking_coords, parkingsLayer)
    
        # Create a MultiGrid object the two layers
        self.grid = mesa.space.MultiGrid(
            width, height, True, (buildingLayer, parkingsLayer,trafficMonitoringLayer)
        )

        #CREATION OF AGENTS IN THE GRID---------------------------------------    
        # Initialize the allowed directions for each cell
        self.initialize_directions(left_coords, right_coords, up_coords, down_coords)

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


    #INITIALIZER METHODS----------------------------------------------------------------------------------
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

            agent = CarAgent(
                self, Spawn, target_parking_spot
            )  # Pass the coordinates

            # Place the agent in the 'Spawn' cell using the correct coordinates
            self.grid.place_agent(agent, Spawn)
    ''' 
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
    '''



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

    def get_global_map(self):
        """
        Generate a global map of the current state of the simulation.
        """
        # Initialize the global map structure
        self.global_map = {
            "Cars": [],
            "Traffic_Lights": {}
        }

        # Collect all CarAgents and TrafficLightAgents
        car_agents = []
        traffic_lights = {}

        for contents, (x, y) in self.grid.coord_iter():
            for agent in contents:
                if isinstance(agent, CarAgent):
                    car_agents.append(agent)
                elif isinstance(agent, TrafficLightAgent):
                    traffic_lights[agent.unique_id] = agent.state  # Map directly to the state

        # Append the positions of the sorted CarAgents to the global_map
        for agent in sorted(car_agents, key=lambda agent: agent.unique_id):
            self.global_map["Cars"].append({"x": agent.pos[0], "y": agent.pos[1]})

        # Append the traffic light data to the global_map
        self.global_map["Traffic_Lights"] = traffic_lights

        # Debug: Print the global map
        print(self.global_map)

        # Return the cars' positions and the traffic lights data
        return {"Cars": self.global_map["Cars"]}, {"Traffic_Lights": self.global_map["Traffic_Lights"]}
    
    # LAYER METHODS----------------------------------------------------------------------------------
    # Set the value of cells to indicate buildings
    def set_building_cells(self, buildings_coords, buildingLayer):
        for coord in buildings_coords:
            buildingLayer.set_cell(coord, 1)

    # Set the value of cells to indicate parking spots
    def set_parking_cells(self, parking_coords, parkingsLayer):

        for coord in parking_coords:
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



