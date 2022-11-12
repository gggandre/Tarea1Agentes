# Importing the Agent class from the mesa module.
from mesa import Agent


# The Roomba class is a subclass of the Agent class. It has a constructor
# that takes a unique_id and a
# model as arguments. It also has a step method that moves the Roomba
# around the grid
class Roomba(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.moves = 0

    def step(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        turn = False
        for cellmate in cellmates:
            if isinstance(cellmate, MugreAgent):
                if not cellmate.is_clean():
                    cellmate.clean()
                    turn = True
                else:
                    self.move()
                    turn = True
        if not turn:
            self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.moves += 1


# > The MugreAgent class is a subclass of the Agent class, and it
# has a unique_id, a model, and a
# dirty attribute
class MugreAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dirty = True

    def step(self):
        pass

    def clean(self):
        self.dirty = False

    def is_clean(self):
        return not self.dirty
