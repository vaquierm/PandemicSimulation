# This file contains the functions to visualize the simulation results
import matplotlib.pyplot as plt

from src.entity_network.person import PersonState


def plot_simulation_results(results: dict):
    """
    Plot the results of the simulation
    :param results: Simulation results dictionary returned by the start method of the simulation
    """
    plt.stackplot(range(len(results[PersonState.Healthy])),
                  [results[PersonState.Incubating], results[PersonState.Sick],
                   results[PersonState.Healthy], results[PersonState.Recovered]],
                  labels=['Asymptomatic', 'Symptomatic', 'Healthy', 'Recovered'],
                  alpha=0.8, colors=['darkorange', 'firebrick', 'steelblue', 'darkgrey'])
    plt.legend(loc='upper right')
    plt.xlabel('Days')
    plt.ylabel('Percentage of population')
    plt.show()
