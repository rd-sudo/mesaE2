import mesa
from mesa.visualization import SolaraViz, make_plot_component, make_space_component

from modelTest import test

def agent_portrayal(agent):
    return {
        "color": "orange",
        "size": 50,
    }

model_params = {
    "count":1,
}

model = test(count = 1, seed=None)

propertylayer_portrayal={"test": {"color":"blue","colorbar":False}}
SpaceGraph = make_space_component(agent_portrayal, propertylayer_portrayal=propertylayer_portrayal) 

page = SolaraViz(
    model,
    components=[SpaceGraph],
    model_params=model_params,
    name="Traffic Simulation",
)
page