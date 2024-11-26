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
        self.cars_in_monitored_area = 0

    def set_state(self, new_state):
        """Change the state of the traffic light."""
        self.state = new_state

    def set_time_counter(self, new_time):
        """Set the time counter of the traffic light."""
        self.time_counter = new_time

    def get_cars_in_monitored_area(self):
        """Check if there are cars in the monitored positions."""
        from CarAgent import CarAgent  # Local import to avoid circular import issue

        self.cars_in_monitored_area = 0
        for pos in self.monitored_positions:
            agents = self.model.grid.get_cell_list_contents([pos])
            for agent in agents:
                if isinstance(agent, CarAgent):
                    self.cars_in_monitored_area += 1
        """Posibly useless code
        if(self.cars_in_monitored_area == 0):
            for pos in self.model.traffic_light_coords[self.traffic_light_id]["position"]:
                agents = self.model.grid.get_cell_list_contents([pos])
                for agent in agents:
                    if isinstance(agent, TrafficLightAgent):
                        agent.set_state("yellow")"""
        return self.cars_in_monitored_area

    def get_group_traffic_lights(self):
        """Get the traffic lights in the group."""
        return self.model.traffic_light_groups[self.group]

    def get_other_traffic_light_id(self):
        """Get the ID of the other traffic light in the same group."""
        for traffic_light_id in self.model.traffic_light_groups[self.group]:
            if traffic_light_id != self.traffic_light_id:
                return traffic_light_id
        return None

    def compare_group_traffic(self):
        other_traffic_light_id = self.get_other_traffic_light_id()
        # print(f"Agent Id: {self.traffic_light_id} | Other traffic light id: {other_traffic_light_id}")
        other_traffic_lights_positions = self.model.traffic_light_coords[
            other_traffic_light_id
        ]["position"]
        self_traffic_light_positions = self.model.traffic_light_coords[
            self.traffic_light_id
        ]["position"]

        other_traffic_lights = []
        self_traffic_lights = []
        for pos in other_traffic_lights_positions:
            agents = self.model.grid.get_cell_list_contents([pos])
            for agent in agents:
                if isinstance(agent, TrafficLightAgent):
                    # print(f"Agent Id: {self.traffic_light_id} | Other traffic_id: {agent.traffic_light_id} | This_id car count: {self.cars_in_monitored_area()} | Other traffic car count: {agent.cars_in_monitored_area()}")
                    other_traffic_lights.append(agent)
                    break

        for pos in self_traffic_light_positions:
            agents = self.model.grid.get_cell_list_contents([pos])
            for agent in agents:
                if isinstance(agent, TrafficLightAgent):
                    # print(f"Agent Id: {self.traffic_light_id} | Other traffic_id: {agent.traffic_light_id} | This_id car count: {self.cars_in_monitored_area()} | Other traffic car count: {agent.cars_in_monitored_area()}")
                    self_traffic_lights.append(agent)
                    break

        other_traffic_light_cars = other_traffic_lights[0].cars_in_monitored_area
        self_traffic_light_cars = self_traffic_lights[0].cars_in_monitored_area

        cars_in_monitored_area = self.cars_in_monitored_area
        if cars_in_monitored_area == 0:
            for traffic_light_agent in self_traffic_lights:
                # Change the state of the other traffic light to red
                traffic_light_agent.set_state("yellow")
        elif cars_in_monitored_area > other_traffic_light_cars:
            # print(f"There are more cars in the monitored area of traffic light {self.traffic_light_id}({self.cars_in_monitored_area()} cars) than in the monitored area of traffic light {other_traffic_light_id}({other_traffic_light_cars} cars)")
            for traffic_light_agent in other_traffic_lights:
                # Change the state of the other traffic light to red
                if traffic_light_agent.cars_in_monitored_area != 0:
                    traffic_light_agent.set_state("red")
                self.set_state("green")

            # print(f"Traffic light {self.traffic_light_id}:{self.position} changed to green and traffic light {other_traffic_light_id} changed to red")

    def step(self):
        self.time_counter += 1
        self.get_cars_in_monitored_area()
        self.compare_group_traffic()
