from mesa.batchrunner import batch_run
from model import CleanModel
import pandas as pd


def execute_model(number_of_agents, width, height, dirty_cells_percentage, max_steps, iterations):
    """
    Runs the model with given parameters and print a dataframe with the results of all the iterations.
    """

    fixed_params = {
        "number_of_agents": number_of_agents,
        "width": width,
        "height": height,
        "dirty_cells_percentage": dirty_cells_percentage
    }

    results = batch_run(
        CleanModel,
        parameters=fixed_params,
        iterations=iterations,
        max_steps=max_steps,
        number_processes=1,
        display_progress=False,
    )

    results_df = pd.DataFrame(results)

    # Rename the columns for more clarity
    results_df.rename(columns={"Step": "Step finished",
                               "number_of_agents": "Number of Agents",
                               "width": "Width of room",
                               "height": "Height of room",
                               "dirty_cells_percentage": "Percentage of dirty cells on Inizialization",
                               "current_clean_cells": "Clean cells on Finalization",
                               "movements": "Movements done by all agents"}, inplace=True)

    # Print only wanted columns
    print(results_df[['iteration',
                      'Step finished',
                      'Number of Agents',
                      'Width of room',
                      'Height of room',
                      'Percentage of dirty cells on Inizialization',
                      'Clean cells on Finalization',
                      'Movements done by all agents']])


if __name__ == "__main__":
    # number of agents in the run
    agents = 5
    # width of the room
    width = 10
    # height of the room
    height = 10
    # percentage of dirty cells on initialization, ex. 20 = 20% of total cells will be dirty
    dirty_cells_percentage = 20
    # max steps of the run
    max_steps = 1000
    # number of times the model will run
    iterations = 10

    execute_model(agents, width, height, dirty_cells_percentage, max_steps, iterations)
