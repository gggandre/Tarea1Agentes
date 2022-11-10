from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from model import CleanModel


NUMBER_OF_CELLS = 10

SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {
    "number_of_agents": UserSettableParameter(
        'slider', 
        "Number of agents", 
        5, # default value
        1,  # min value
        100,  # max value
        1, # step
        description="Choose how many agents to include in the model"),

    "width": UserSettableParameter(
        'slider',
        "Width",
        10,
        5,
        30,
        1,
        description="Choose the width of the grid"),
    
    "height": UserSettableParameter(
        'slider',
        "Height",
        10,
        5,
        30,
        1,
        description="Choose the height of the grid"),

    "dirty_cells_percentage": 20

}

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5,
                 "Layer": 0,
                 "Color": "red",
                 "text": agent.unique_id,
                 "text_color": "black"}
    return portrayal

grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)

chart_currents = ChartModule(
    [
        {"Label": "current_clean_cells", "Color": "Black"}
    ],
    data_collector_name='datacollector'
)

server = ModularServer(CleanModel,
                          [grid, chart_currents],
                            "Clean Model",
                            simulation_params)

server.port = 8521 # The default
server.launch()
