"""
City Simulation Model
=============================================================
A Mesa implementation of a city simulation model, where the cars
move randomly around the city and go to the parking spots in there
"""

import mesa
import time

# Data visualization tools.
import seaborn as sns
import random
import numpy as np

# Data manipulation and analysis.
import pandas as pd

from agent import CarAgent


buildings_coords = [
    (2, 2),
    (2, 3),
    (2, 6),
    (2, 7),
    (2, 12),
    (2, 13),
    (2, 15),
    (2, 16),
    (2, 17),
    (2, 18),
    (2, 19),
    (2, 20),
    (2, 21),
    (3, 2),
    (3, 3),
    (3, 7),
    (3, 12),
    (3, 13),
    (3, 14),
    (3, 15),
    (3, 16),
    (3, 17),
    (3, 18),
    (3, 19),
    (3, 20),
    (4, 2),
    (4, 6),
    (4, 7),
    (4, 13),
    (4, 14),
    (4, 15),
    (4, 16),
    (4, 17),
    (4, 18),
    (4, 19),
    (4, 20),
    (4, 21),
    (5, 2),
    (5, 3),
    (5, 6),
    (5, 7),
    (5, 12),
    (5, 13),
    (5, 14),
    (5, 15),
    (5, 16),
    (5, 18),
    (5, 19),
    (5, 20),
    (5, 21),
    (8, 2),
    (8, 3),
    (8, 6),
    (8, 7),
    (8, 12),
    (8, 13),
    (8, 14),
    (8, 16),
    (8, 19),
    (8, 20),
    (8, 21),
    (9, 3),
    (9, 6),
    (9, 7),
    (9, 12),
    (9, 13),
    (9, 14),
    (9, 15),
    (9, 16),
    (9, 19),
    (9, 20),
    (9, 21),
    (10, 2),
    (10, 3),
    (10, 6),
    (10, 13),
    (10, 14),
    (10, 15),
    (10, 16),
    (10, 20),
    (10, 21),
    (11, 2),
    (11, 3),
    (11, 6),
    (11, 7),
    (11, 12),
    (11, 13),
    (11, 14),
    (11, 15),
    (11, 16),
    (11, 19),
    (11, 20),
    (11, 21),
    (13, 9),
    (13, 10),
    (14, 9),
    (14, 10),
    (16, 2),
    (16, 3),
    (16, 4),
    (16, 5),
    (16, 6),
    (16, 7),
    (16, 12),
    (16, 13),
    (16, 14),
    (16, 15),
    (16, 18),
    (16, 19),
    (16, 20),
    (16, 21),
    (17, 2),
    (17, 3),
    (17, 5),
    (17, 7),
    (17, 12),
    (17, 13),
    (17, 14),
    (17, 15),
    (17, 18),
    (17, 19),
    (17, 20),
    (18, 12),
    (18, 13),
    (18, 14),
    (18, 15),
    (18, 18),
    (18, 19),
    (18, 20),
    (18, 21),
    (19, 12),
    (19, 13),
    (19, 14),
    (19, 15),
    (19, 18),
    (19, 19),
    (19, 20),
    (19, 21),
    (20, 2),
    (20, 3),
    (20, 5),
    (20, 6),
    (20, 7),
    (20, 12),
    (20, 13),
    (20, 14),
    (20, 19),
    (20, 20),
    (20, 21),
    (21, 2),
    (21, 3),
    (21, 4),
    (21, 5),
    (21, 6),
    (21, 7),
    (21, 12),
    (21, 13),
    (21, 14),
    (21, 15),
    (21, 18),
    (21, 19),
    (21, 20),
    (21, 21),
]

parking_spots = (
    [(2, 14)]
    + [(3, 21)]
    + [
        # 3
        (3, 6)
    ]
    + [
        # 4
        (4, 12)
    ]
    + [
        # 5
        (4, 3)
    ]
    + [
        # 6
        (5, 17)
    ]
    + [
        # 7
        (8, 15)
    ]
    + [
        # 8
        (9, 2)
    ]
    + [
        # 9
        (10, 19)
    ]
    + [
        # 10
        (10, 12)
    ]
    + [
        # 11
        (10, 7)
    ]
    + [
        # 12
        (17, 21)
    ]
    + [
        # 13
        (17, 6)
    ]
    + [
        # 14
        (17, 4)
    ]
    + [
        # 15
        (20, 18)
    ]
    + [
        # 16
        (20, 15)
    ]
    + [
        # 17
        (20, 4)
    ]
)


# Traffic Model


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
        parkings_coords=None,
    ):
        super().__init__()
        # Properties for the grid
        buildingLayer = mesa.space.PropertyLayer(
            "building", width, height, np.int64(0), np.int64
        )
        parkingsLayer = mesa.space.PropertyLayer(
            "parking", width, height, np.int64(0), np.int64
        )

        # Set the building and parking cells
        self.set_building_cells(buildings_coords, buildingLayer)
        self.set_parking_cells(parkings_coords, parkingsLayer)

        self.parkings_coords = parkings_coords
        self.width = width
        self.height = height
        self.num_agents = num_agents
        self.grid = mesa.space.MultiGrid(
            width, height, True, (buildingLayer, parkingsLayer)
        )
        self.random = random.Random()
        self.steps = 0
        self.sema_coords = [
            [(8, 22), (8, 23)],
            [(8, 18), (8, 17)],
            [(6, 21), (7, 21)],
            [(6, 16), (7, 16)],
            [(6, 2), (7, 2)],
            [(0, 6), (1, 6)],
            [(2, 4), (2, 5)],
            [(5, 0), (5, 1)],
            [(17, 8), (17, 9)],
            [(18, 7), (19, 7)],
        ]

        # Dictionary to store the global map of the city
        self.global_map = {}

        self.ParkingSpots = {
            1: (2, 14),
            2: (3, 21),
            3: (3, 6),
            4: (4, 12),
            5: (4, 3),
            6: (5, 17),
            7: (8, 15),
            8: (9, 2),
            9: (10, 19),
            10: (10, 12),
            11: (10, 7),
            12: (17, 21),
            13: (17, 6),
            14: (17, 4),
            15: (20, 18),
            16: (20, 15),
            17: (20, 4),
        }
        # Dictionary to store directions for each cell
        self.directions = {}

        # Crear agentes y colocarlos en el grid
        used_parking_spots = set()

        for i in range(num_agents):

            available_spawn_spots = [
                spot
                for spot in self.ParkingSpots.values()
                if spot not in used_parking_spots
            ]

            if available_spawn_spots:
                Spawn = random.choice(available_spawn_spots)
            else:
                # Si no hay spots disponibles, puedes tomar alguna acción (puedes hacer un break o algo similar)
                print("No available spots for spawn")
                break

            used_parking_spots.add(Spawn)

            # Crear una lista de spots disponibles para el parking objetivo (que no sean el de Spawn ni los usados)
            available_target_spots = [
                spot
                for spot in self.ParkingSpots.values()
                if spot != Spawn and spot not in used_parking_spots
            ]

            if available_target_spots:
                target_parking_spot = random.choice(available_target_spots)
            else:
                # Si no hay spots disponibles, tomar alguna acción (ej. break o continuar)
                print("No available spots for target parking")
                break  # o continuar con alguna otra acción que desees.

            # Marcar el spot objetivo como utilizado
            used_parking_spots.add(target_parking_spot)

            print(f"Spawn: ({Spawn}), Target: ({target_parking_spot})")

            agent = CarAgent(
                self, Spawn, target_parking_spot
            )  # Pasa las coordenadas desglosadas

            # Colocar el agente en la celda 'Spawn' usando las coordenadas correctas
            self.grid.place_agent(agent, Spawn)

        # Inicializar las direcciones permitidas para cada celda
        self.initialize_directions(left_coords, right_coords, up_coords, down_coords)

        # Colocar los semáforos en el grid
        self.place_semaphore_agents()

        # Initialize the DataCollector
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "NumAgents": "num_agents",
            },
            agent_reporters={
                "Position": "pos",
                "TargetParkingSpot": lambda agent: (
                    agent.target_parking_spot if isinstance(agent, CarAgent) else None
                ),
            },
        )

        # Collect initial data
        self.datacollector.collect(self)

    def initialize_directions(self, left_coords, right_coords, up_coords, down_coords):
        # Inicializar todas las coordenadas del grid con todas las direcciones en False
        for x in range(self.width):
            for y in range(self.height):
                self.directions[(x, y)] = {
                    "left": False,
                    "right": False,
                    "up": False,
                    "down": False,
                }

        # Configurar direcciones específicas para cada lista
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

    def get_cell_directions(self, pos):
        # Fetch the direction info for a specific cell
        return self.directions.get(pos, None)

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

        # Add the current step and agents' positions to the global_map
        step_number = self.steps
        if step_number not in self.global_map:
            self.global_map[step_number] = []

        # Collect all CarAgents and sort them by unique_id
        car_agents = []
        for contents, x, y in self.grid.coord_iter():
            for agent in contents:
                if isinstance(agent, CarAgent):
                    car_agents.append(agent)

        car_agents.sort(key=lambda agent: agent.unique_id)

        # Append the positions of the sorted CarAgents to the global_map
        for agent in car_agents:
            self.global_map[step_number].append(agent.pos)

    def place_semaphore_agents(self):
        # Iterar sobre cada semáforo en sema_coords y asignar un ID único para cada par
        for idx, semaforo in enumerate(self.sema_coords):
            semaforo_id = f"sema_{idx}"  # ID único para cada semáforo

            # Crear dos agentes separados con el mismo id y colocarlos en las posiciones correspondientes
            for pos in semaforo:
                sema_agent = SemaphoreAgent(semaforo_id, self)  # Asigna el mismo id
                self.grid.place_agent(sema_agent, pos)
        """This dictionary is going to look like this:
            {Number_of_Step1: [(x1, y1), (x2, y2), ...],
            Number_of_Step2: [(x1, y1), (x2, y2), ...]
            Number_of_StepN: [(x1, y1), (x2, y2), ...]}
        """

    # VIZUALIZATION
    def set_building_cells(self, buildings_coords, buildingLayer):
        for coord in buildings_coords:
            buildingLayer.set_cell(
                coord, 1
            )  # Establecer el valor de la celda a 1 para indicar un edificio

    def set_parking_cells(self, parking_coords, parkingsLayer):
        for coord in parking_coords:
            parkingsLayer.set_cell(
                coord, 1
            )  # Establecer el valor de la celda a 1 para indicar un edificio
