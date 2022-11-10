from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from modelo_dinero import MoneyModel
from mesa.visualization.modules import CanvasGrid

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
server = ModularServer(MoneyModel,
                       [grid],
                       "Money Model",
                       {"N": 10, "width": 10, "height": 10})
server.port = 8521 # The default
server.launch()
