# M1. Actividad
# Erika García A01745158
# David Damián A01752785

import mesa


def compute_clean_cells(model):
    # print(model.height)
    cells = model.height * model.width
    dirty_cells = 0
    for agent in model.schedule.agents:
        if isinstance(agent, DirtynessAgent):
            if not agent.is_clean():
                dirty_cells += 1
    clean_ratio = (cells - dirty_cells) / cells * 100
    # print(clean_ratio)
    return clean_ratio
    # agent_wealths = [agent.wealth ]
    # x = sorted(agent_wealths)
    # N = model.num_agents
    # B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    # return 1 + (1 / N) - 2 * B


def compute_agent_moves(model):
    movements = 0
    for agent in model.schedule.agents:
        if isinstance(agent, AspiradoraAgent):
            movements += agent.moves
    return movements

class DirtynessAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dirty = True

    def step(self):
        pass

    def clean(self):
        self.dirty = False

    def is_clean(self):
        return not self.dirty


class AspiradoraAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.moves = 0

    def step(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        turn = False
        for cellmate in cellmates:
            if isinstance(cellmate, DirtynessAgent):
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


class AspiradoraModel(mesa.Model):
    def __init__(self, width, height, num_agents,
                 dirty_percentage, max_steps):
        self.num_agents = num_agents
        self.width = width
        self.height = height
        self.dirty_percentage = dirty_percentage
        self.remaining_steps = max_steps
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        num_dirty_cells = int(self.dirty_percentage * width * height)
        used_coordinates = set()
        for i in range(num_dirty_cells):
            agent = DirtynessAgent(i, self)
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while (x, y) in used_coordinates:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            used_coordinates.add((x, y))

        for i in range(self.num_agents):
            agent = AspiradoraAgent(i + num_dirty_cells, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))

        self.datacollector = mesa.DataCollector(
            model_reporters={"CleanCells": compute_clean_cells,
                             "TotalMovements": compute_agent_moves}
        )

    def step(self):
        if self.remaining_steps > 0 and compute_clean_cells(self) != 100.0:
            self.datacollector.collect(self)
            self.schedule.step()
            self.remaining_steps -= 1


if __name__ == '__main__':
    width_param = int(input("Ingrese ancho:"))
    height_param = int(input("Ingrese alto:"))
    num_agents_param = int(input("Ingrese el numero de agentes:"))
    dirty_percentage_param = \
        float(input("Ingrese el porcentaje de casillas sucias (0 a 1):"))
    max_steps_param = int(input("Ingrese el numero de pasos maximos:"))
    iterations_param = int(input("Ingrese el numero de iteraciones:"))
    params = {"width": width_param,
              "height": height_param,
              "num_agents": num_agents_param,
              "dirty_percentage": dirty_percentage_param,
              "max_steps": max_steps_param + 1}

    results = mesa.batch_run(
        AspiradoraModel,
        parameters=params,
        iterations=iterations_param,
        max_steps=max_steps_param,
        number_processes=1,
        data_collection_period=1,
        display_progress=True,
    )

    import pandas as pd
    results_df = pd.DataFrame(results)
    clean_cells = []
    total_movements = []
    for i in range(iterations_param):
        # Obtain the row containing the general outcome of the
        # i-th run
        run_info = results_df.query(f'RunId == {i}') \
            .nlargest(1, 'TotalMovements')
        print(run_info)
        clean_cells.append(run_info.iloc[0]['CleanCells'])
        total_movements.append(run_info.iloc[0]['TotalMovements'])
    
    import matplotlib.pyplot as plt
    plt.hist(clean_cells, bins=20)
    plt.show()
    plt.hist(total_movements, bins=20)
    plt.show()
    # print(clean_cells)
    # print(results_df.to_string())
    # print(results_df.keys())
    # print(results_df['CleanCells'])
    # print(results_df['TotalMovements'])
    
    # import matplotlib.pyplot as plt
    # # Run the model
    # model = AspiradoraModel(30, 20, 1, 0.2, 1000)
    # for i in range(50):
    #     model.step()

    # clean_cells = model.datacollector.get_model_vars_dataframe()
    # clean_cells.head()
    # clean_cells.plot()
    # plt.show()

    # gini = model.datacollector.get_model_vars_dataframe()
    # gini.plot()
    # plt.show()
    # end_wealth = agent_wealth.xs(99, level="Step")["Wealth"]
    # end_wealth.hist(bins=range(agent_wealth.Wealth.max() + 1))
    # plt.show()
    # one_agent_wealth = agent_wealth.xs(14, level="AgentID")
    # one_agent_wealth.Wealth.plot()
    # plt.show()

    # # save the model data (stored in the pandas gini object) to CSV
    # gini.to_csv("model_data.csv")

    # # save the agent data (stored in the pandas agent_wealth object) to CSV
    # agent_wealth.to_csv("agent_data.csv")

    # params = {"width": 10, "height": 10, "N": range(10, 500, 10)}

    # results = mesa.batch_run(
    #     MoneyModel,
    #     parameters=params,
    #     iterations=5,
    #     max_steps=100,
    #     number_processes=1,
    #     data_collection_period=1,
    #     display_progress=True,
    # )

    # import pandas as pd

    # results_df = pd.DataFrame(results)
    # print(results_df.keys())

    # results_filtered = results_df[(results_df.AgentID == 0) & (results_df.Step == 100)]
    # N_values = results_filtered.N.values
    # gini_values = results_filtered.Gini.values
    # plt.scatter(N_values, gini_values)
    # plt.show()
