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

    plt.plot(range(len(results[PersonState.Healthy])), results['average_new_cases'], color='firebrick', linewidth=3, label='Average new cases over 7 days')
    plt.plot(range(len(results[PersonState.Healthy])), results['new_cases'], color='lightcoral', alpha=0.5, linewidth=1, label='New cases')
    plt.legend(loc='upper right')
    plt.xlabel('Days')
    plt.ylabel('New cases in percentage of total population')
    plt.show()
