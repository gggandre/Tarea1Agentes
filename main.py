# Importing the libraries that are used in the code.
from mesa import Agent, Model
from mesa.space import MultiGrid
# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que
# fuerza un solo objeto por celda.
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import numpy as np
import time
import datetime
import random


def obtener_cuadricula(model):
    """
    It creates a grid of zeros, then iterates over every cell in the grid, and if the cell contains a
    robot, it sets the value of that cell to 2, and if the cell contains a dirt patch, it sets the value
    of that cell to 1
    :param model: The model object
    :return: a grid of the model.
    """
    cuadricula = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        for obj in cell_content:
            if isinstance(obj, RobotLimpiezaReactivo):
                cuadricula[x][y] = 2
            elif isinstance(obj, CeldadelRobot):
                cuadricula[x][y] = obj.status
    return cuadricula


class RobotLimpiezaReactivo(Agent):
  def __init__(self, id, model):
    """
    A constructor that initializes the attributes of the class.
    
    :param id: The id of the agent
    :param model: The model that the agent is in
    """
    super().__init__(id, model)
    self.siguiente = None
    self.mov1 = 0
    self.movimientos2 = 0

  def step(self):
    """
    If the robot is in the same cell as another robot, and that other robot is in state 1, then the
    other robot will go to state 0, and this robot will stay in the same cell. If the other robot is in
    state 0, then this robot will move to a random cell.
    """
    neighbors = self.model.grid.get_neighbors(
        self.pos, 
        moore = True,
        include_center = True)
    for neighbor in neighbors:
      if isinstance(neighbor, CeldadelRobot) and self.pos == neighbor.pos:
        if neighbor.status == 1:
          neighbor.siguiente = 0
          self.siguiente = self.pos
        else: #vecino.estado == 0
          self.mov1 += 1
          second_neighbor = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = False)
          neighbor.siguiente = 0
          self.siguiente = self.random.choice(second_neighbor)
        break

  def advance(self): 
    """
    If the agent is in the same cell as another agent, then the other agent's status is set to the other
    agent's next status.
    """
    neighbors = self.model.grid.get_neighbors(
        self.pos, 
        moore = True,
        include_center = True)
# Moving the robot to the next cell.
    for neighbor in neighbors:
      if isinstance(neighbor, CeldadelRobot) and self.pos == neighbor.pos:
        neighbor.status = neighbor.siguiente
        break
    self.model.grid.move_agent(self, self.siguiente)


# The class CeldadelRobot is a subclass of the class Agent. It has three attributes: pos, status, and
# siguiente. The constructor initializes the attributes
class CeldadelRobot(Agent):
    # 1 celda sucia
    # 0 celda limpia

  def __init__(self, id, model, status):
    """
    The function __init__() is a special function in Python classes. It is known as a constructor in
    object oriented concepts. This function is called when an object is created from a class and it
    allows the class to initialize the attributes of the class
    
    :param id: The id of the car
    :param model: The model of the car
    :param status: 0 = not infected, 1 = infected, 2 = recovered
    """
    super().__init__(id, model)
    self.pos = id
    self.status = status
    self.siguiente = None

# It creates a grid, places agents in it, and then runs the simulation.
class Lugar(Model):
  def __init__(self, M, N, agentes, celdas_sucias):
    """
    The function __init__() is a special function in Python classes. It is known as a constructor in
    object oriented concepts. This function is called when an object is created from a class and it
    allows the class to initialize the attributes of the class.
    
    :param M: number of rows in the grid
    :param N: number of columns
    :param agentes: number of agents
    :param celdas_sucias: The percentage of cells that are dirty
    """
    self.num_agentes = agentes
    self.porc_celdas_sucias = celdas_sucias
    self.porc_celdas_limpias = 1 - celdas_sucias
    self.grid = MultiGrid(M, N, False)
    self.schedule = SimultaneousActivation(self)

# Creating the grid and placing the agents in it.
    celdassuciasnum = int(M * N * celdas_sucias)
    for(content, x, y) in self.grid.coord_iter():
      num = random.randint(0, 1)
      if num == 1 and celdassuciasnum > 0:
        a = CeldadelRobot((x, y), self, 1)
        celdassuciasnum -= 1
      else:
        a = CeldadelRobot((x, y), self, 0)
      self.grid.place_agent(a, (x, y))
      self.schedule.add(a)

# Creating the agents and placing them in the grid.
    for id in range(agentes):
      r = RobotLimpiezaReactivo(id, self)
      self.grid.place_agent(r, (1,1))
      self.schedule.add(r)
    self.datacollector = DataCollector(
        model_reporters = {"Grid": obtener_cuadricula})

  def step(self):
    """
    The function step() is called on the model object, which in turn calls the step() function on the
    scheduler object, which in turn calls the step() function on each agent object
    """
    self.datacollector.collect(self)
    self.schedule.step()

  def robotlimpio(self):
    """
    If there is a cell with a robot in it, and the robot is dirty, then the robot is not clean
    :return: a boolean value.
    """
    for (content, x, y) in self.grid.coord_iter():
      for obj in content:
        if isinstance(obj, CeldadelRobot) and obj.status == 1:
          return False
    return True

  def celdas_sucias(self):
    """
    It counts the number of cells that have a CeldadelRobot object in them and that have a status of 1
    :return: The number of dirty cells.
    """
    celdas_sucias = 0
    for (content, x, y) in self.grid.coord_iter():
      for obj in content:
        if isinstance(obj, CeldadelRobot) and obj.status == 1:
          celdas_sucias = celdas_sucias + 1
    return celdas_sucias


  def movimientos_robot(self, M, N, agentes):
    """
    It counts the number of times the robot has moved
    
    :param M: number of rows
    :param N: number of rows
    :param agentes: number of agents
    :return: The number of movements of the robots.
    """
    contador = 0
    for i in range (N*M, N*M + agentes):
      contador = contador + self.schedule.agents[i].mov1
    return contador


# Número de espacios M x N
# Setting the variables for the model.
M = 4
N = 4
agentes = 1
cantidad_sucias = 0.6
maxtime = 0.5
contador = 0
movimientos = 0

model = Lugar(M, N, agentes, cantidad_sucias)
start_time = time.time()
# A while loop that runs until the time is less than maxtime and the robot is not clean.
while ((time.time() - start_time) < maxtime and not model.robotlimpio()):
    model.step()
    contador = contador + 1
movimientos = model.movimientos_robot(M, N, agentes)
all_grid = model.datacollector.get_model_vars_dataframe()
# Printing the grid, the time, the number of dirty cells, the number of movements and the number of
# frames used.
print(all_grid.to_string())
print("Tiempo: ", str(datetime.timedelta(seconds=(time.time() - start_time))))
print("Celdas sucias: ", str(model.celdas_sucias()))
print('Movimientos de los agentes: ', str(movimientos))
print('Cuadros usados: ', str(contador))


class RobotLimpiador(Model):
    '''
    Define el modelo del juego de la vida.
    '''
    def __init__(self, width, height):
        self.num_agentes = width * height
        self.grid = SingleGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True  # Para la visualizacion usando navegador

        for (content, x, y) in self.grid.coord_iter():
            a = RobotLimpiador((x, y), self)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)

    def step(self):
        self.schedule.step()
