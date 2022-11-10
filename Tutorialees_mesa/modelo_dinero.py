from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agente_dinero import MoneyAgent


class MoneyModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        # Creacion de los agentes
        for i in range (self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            
            # Agrega el agente a una celda aleatoria
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
    
    def step(self):
        self.schedule.step()
        
        