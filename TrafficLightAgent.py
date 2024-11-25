import mesa


class TrafficLightAgent(mesa.Agent):
    def __init__(
        self, traffic_light_id, state, model, group, position, monitored_positions
    ):
        super().__init__(model)
        self.traffic_light_id = traffic_light_id
        self.state = state
        self.time_counter = 0
        self.group = group
        self.position = position
        self.monitored_positions = monitored_positions

    def change_state(self, new_state):
        """Change the state of the traffic light."""
        self.state = new_state

    def check_cars(self):
        """Check if there are cars in the monitored positions."""
        in_area_cars = 0
        for pos in self.monitored_positions:
            agents = self.model.grid.get_cell_list_contents([pos])
            for agent in agents:
                if isinstance(agent, CarAgent):
                    in_area_cars += 1
        return in_area_cars

    def sync_with_group(self):
        """Synchronize the state of the traffic light with the group."""
        for pos in self.position:
            agents = self.model.grid.get_cell_list_contents([pos])
            for agent in agents:
                if isinstance(agent, TrafficLightAgent) and agent.group == self.group:
                    agent.change_state(self.state)

    def step(self):
        self.time_counter += 1
        if self.time_counter >= 10:
            self.change_state()
            self.time_counter = 0
