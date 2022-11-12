from mesa import Agent


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
    