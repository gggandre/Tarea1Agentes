from mesa import Agent


class Robot(Agent):
    """ Un agente que va a hacer la limpieza del cuarto. """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        """ The robot moves if it's not dirty, otherwise it cleans the cell """
        if self.pos in self.model.dirty_cells:
            self.clean()
        else:
            self.move()

    def move(self):
        """ El robot se mueve en una dirección aleatoria. """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )

        # If the number of possible steps is less than 0, add fillers to simulate a non possible movement
        while len(possible_steps) < 8:
            possible_steps.append((-1, -1))

        new_position = self.random.choice(possible_steps)

        # If the new position is not a valid position, do not move
        if new_position != (-1, -1):
            self.model.grid.move_agent(self, new_position)
            self.model.add_movement()
            # print("El robot se movió a la posición: ", new_position)
        else:
            # print("El robot no se movió.")
            pass

    def clean(self):
        """ The robot cleans the cell """
        self.model.dirty_cells.remove(self.pos)
        # print("El robot limpió la celda: ", self.pos)
