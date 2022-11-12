# Importing the modules that are needed for the model to run.
from mesa import Model
from agent import Roomba
from agent import MugreAgent, Roomba
from mesa import time
from mesa import space
from mesa import DataCollector


def compute_clean_cells(model):
    """
    It computes the percentage of clean cells in the grid
    :param model: the model object
    :return: The percentage of clean cells in the grid.
    """
    cells = model.height * model.width
    dirty_cells = 0
    for agent in model.schedule.agents:
        if isinstance(agent, MugreAgent):
            if not agent.is_clean():
                dirty_cells += 1
    clean_ratio = (cells - dirty_cells) / cells * 100
    return clean_ratio


def compute_agent_moves(model):
    """
    It counts the number of moves made by all Roomba agents in the model
    :param model: the model object
    :return: The number of movements of all the Roomba agents.
    """
    movements = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Roomba):
            movements += agent.moves
    return movements


def tiempo(model):
    """
    It returns the current time of the model
    :param model: the model object
    :return: The time of the model.
    """
    return model.schedule.time


# It creates a grid, places agents on the grid, and then creates
# a data collector
class RoombaModel(Model):
    def __init__(self, width, height, num_agents,
                 dirty_percentage, max_steps):
        """
        It creates a grid, places agents on the grid, and then creates
        a data collector.
        :param width: The width of the grid
        :param height: The height of the grid
        :param num_agents: number of agents
        :param dirty_percentage: percentage of the grid that is dirty
        :param max_steps: The number of steps the simulation will run for
        """
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
        """
        The function step() is called by the run_model() function. It checks
        if the number of steps is greater than 0 and if the number of clean
        cells is not equal to 100. If both conditions are true,
        the function collects data and then steps through the schedule
        """
        if self.remaining_steps > 0 and compute_clean_cells(self) != 100.0:
            self.datacollector.collect(self)
            self.schedule.step()
            self.remaining_steps -= 1
