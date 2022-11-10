from mesa import Agent

class Roomba(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pos = 0
        
    def step(self):
        if self.pos in self.model.basura:
            self.limpia_celda()
        else:
            self.move()
            
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        self.moves += 1
        