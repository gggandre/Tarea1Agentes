from mesa import Model
from agent import Roomba
from agent import MugreAgent, Roomba
from mesa import time
from mesa import space
from mesa import DataCollector
import mesa

def compute_clean_cells(model):
    
    cells = model.height * model.width
    dirty_cells = 0
    for agent in model.schedule.agents:
        if isinstance(agent, MugreAgent):
            if not agent.is_clean():
                dirty_cells += 1
    clean_ratio = (cells - dirty_cells) / cells * 100
    
    return clean_ratio
   

def compute_agent_moves(model):
    movements = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Roomba):
            movements += agent.moves
    return movements


def tiempo(model):
    return model.schedule.time


class RoombaModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, height, num_agents,
                 dirty_percentage, max_steps):
        
        self.num_agents = num_agents
        self.width = width
        self.height = height
        self.dirty_percentage = dirty_percentage
        self.remaining_steps = max_steps
        self.grid = space.MultiGrid(width, height, False)
        self.schedule = time.RandomActivation(self)
        self.running = True
        
        num_dirty_cells = int(self.dirty_percentage * width * height)
        used_coordinates = set()
        
        for i in range(num_dirty_cells):
            agent = MugreAgent(i, self)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            while (x, y) in used_coordinates:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            used_coordinates.add((x, y))

        for i in range(self.num_agents):
            agent = Roomba(i + num_dirty_cells, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))

        self.datacollector = DataCollector(
            model_reporters={"% Celdas Limpias": compute_clean_cells,
                             "Movimientos": compute_agent_moves,
                             "Tiempo": tiempo})

    def step(self):
        if self.remaining_steps > 0 and compute_clean_cells(self) != 100.0:
            self.datacollector.collect(self)
            self.schedule.step()
            self.remaining_steps -= 1
