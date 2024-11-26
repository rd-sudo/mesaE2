import mesa


class TrafficLightAgent(mesa.Agent):
    def __init__(self, unique_id, state, model, group=None):
        """
        Initialize a TrafficLightAgent.

        Args:
            unique_id (str): Unique identifier for the traffic light.
            state (str): Initial state of the traffic light ("red" or "green").
            model (Model): The model instance that contains this agent.
        """
        super().__init__(model)
        self.unique_id = unique_id
        self.state = state
        self.time_counter = 0
        self.group = group

    def change_state(self, state):
        """Change the state of the traffic light."""
        self.state = state

    def step(self):
        """
        Advance the traffic light by one step.

        The traffic light changes state every 30 steps.
        """
        self.time_counter += 1
        if self.time_counter >= 10:
            self.change_state()
            self.time_counter = 0
