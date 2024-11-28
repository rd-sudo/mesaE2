import mesa
from CarAgent import CarAgent


class TrafficLightAgent(mesa.Agent):
    def __init__(self, unique_id, state, model, monitored_positions):
        super().__init__(model)
        self.unique_id = f"sema_{unique_id}"
        self.state = state
        self.time_counter = 0
        self.monitored_positions = monitored_positions
        self.neighbor_siblings = []
        self.neighbor_opposites = []

    def update_neighbors(self):
        """Actualiza las listas de semáforos hermanos y opuestos."""
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=True, include_center=False
        )

        self.neighbor_siblings = [
            agent
            for agent in neighbors
            if isinstance(agent, TrafficLightAgent)
            and agent.unique_id == self.unique_id
        ]
        self.neighbor_opposites = [
            agent
            for agent in neighbors
            if isinstance(agent, TrafficLightAgent)
            and agent.unique_id != self.unique_id
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

        for sibling in self.neighbor_siblings:
            sibling_traffic = sibling.cars_in_monitored_area()

        for opposite in self.neighbor_opposites:
            opposite_traffic = opposite.cars_in_monitored_area()

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
                if opposite_traffic == 0:
                    opposite_traffic = 3
                else:
                    opposite.state = 1

                tempSelf = opposite
                for sibling in self.neighbor_siblings:
                    sibling.state = self.state
            elif current_traffic == opposite_traffic:
                self.state = 2
                opposite.state = 1
                tempSelf = opposite
                for sibling in self.neighbor_siblings:
                    sibling.state = self.state

        # Obtener vecinos de tempSelf
        if tempSelf:
            tempSelf_neighbors = self.model.grid.get_neighbors(
                tempSelf.pos, moore=True, include_center=False
            )
            tempSelf_traffic_lights = [
                agent
                for agent in tempSelf_neighbors
                if isinstance(agent, TrafficLightAgent)
            ]

            for neighbor in tempSelf_traffic_lights:
                neighbor_traffic = neighbor.cars_in_monitored_area()

                if tempSelf.unique_id == neighbor.unique_id:
                    neighbor.state = tempSelf.state

    def step(self):
        """Actualizar el estado en cada paso."""
        self.time_counter += 1
        self.update_neighbors()  # Asegurarse de que las listas de vecinos estén actualizadas.
        self.compare_traffic_with_neighbors()
