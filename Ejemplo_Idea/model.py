from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agent import Robot
import random
from mesa.datacollection import DataCollector


class CleanModel(Model):
    def __init__(self, number_of_agents, width, height, dirty_cells_percentage):
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, False)
        # Variable to count all movements across all agents
        self.movements = 0
        self.schedule = RandomActivation(self)
        # Get the number of dirty cells according to the parameter
        self.dirty_cells = self.get_random_grid_cells(width * height * dirty_cells_percentage // 100)

        self.running = True

        # Collect data about current clean cells and movements across all agents
        self.datacollector = DataCollector(
            {
                "current_clean_cells": CleanModel.current_clean_cells,
                "movements": CleanModel.get_movements
            }
        )

        # Create agents
        for i in range(self.num_agents):
            a = Robot(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            self.grid.place_agent(a, (1, 1))

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        # if there are no dirty cells, stop the simulation
        if CleanModel.current_clean_cells(self) == 100:
            self.running = False

    def get_random_grid_cells(self, cell_count):
        """ Devuelve una lista de celdas aleatorias que no se repiten. """
        all_cells = [(x[1], x[2]) for x in self.grid.coord_iter()]
        return random.sample(all_cells, cell_count)

    def current_clean_cells(self):
        # Get the number of clean cells in the model
        return self.grid.width * self.grid.height - len(self.dirty_cells)

    def add_movement(self):
        # Add a movement to the total movements
        self.movements += 1

    def get_movements(self):
        # Get the total movements
        return self.movements
