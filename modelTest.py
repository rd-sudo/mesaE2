import mesa
import numpy as np

class TestModel(mesa.Model):
    def __init__(self, count, seed=None):
        super().__init__(seed=seed)
        self.width = 5
        self.height = 5

        # Initialize the PropertyLayer directly
        self.test_layer = mesa.space.PropertyLayer("test", self.width, self.height, initial_value=0)
        
        # Initialize the MultiGrid without including the PropertyLayer in its parameters
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)
        self.running = True

        # Set a cell property
        self.test_layer.set_cell((0, 0), 1)

        # Print the property value for debugging
        print(f"Value at (0, 0): {self.test_layer.get_cell((0, 0))}")

        # Add agents (if needed)
        for i in range(count):
            agent = mesa.Agent(i, self)
            self.grid.place_agent(agent, (i % self.width, i // self.width))

    def step(self):
        pass

# Instantiate the model
model = TestModel(count=10)
