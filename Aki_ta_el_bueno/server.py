import mesa

from model import RoombaModel
from agent import MugreAgent


def agent_portrayal(agent):
    mugre = {"Shape": "circle", "Filled": "true", "r": 0.7}
    roomba = {"Shape": "rect", "Filled": "true", "w": 1, "h": 1}

    if type(agent) is MugreAgent:
        if not agent.is_clean():
            mugre["Color"] = "red"
            mugre["Layer"] = 5
            
        else:
            mugre["Color"] = "green"
            mugre["Layer"] = 5
    
    else:
        roomba["Color"] = "brown"
        roomba["Layer"] = 10
    return mugre if type(agent) is MugreAgent else roomba


if __name__ == '__main__':
    width: int = int(input("Ancho: "))
    height: int = int(input("Alto: "))
    grid = mesa.visualization.CanvasGrid(
        agent_portrayal, width, height, 500, 500)
    model_params = {
        "num_agents": mesa.visualization.Slider(
            "Numero de agentes",
            1,
            1,
            50,
            1,
            description="Choose how many agents to include in the model",
        ),
        "dirty_percentage": mesa.visualization.Slider(
            "% Mugre",
            0.2,
            0,
            1,
            0.01,
            description="Choose the percentage of dirty cells",
        ),
        "max_steps": mesa.visualization.Slider(
            "Pasos",
            100,
            10,
            10000,
            1,
            description="Choose the maximum number of steps"
        ),
        "width": width,
        "height": height,
    }
    server = mesa.visualization.ModularServer(
        RoombaModel, [grid], "RoombaModel", model_params
    )
    server.port = 8521
    server.launch()
