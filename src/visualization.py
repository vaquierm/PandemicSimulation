# This file contains the functions to visualize the simulation results
import matplotlib.pyplot as plt

from src.entity_network.person import PersonState


def __plot_trigger(results, trigger_name: str):
    t = results[trigger_name]
    _, y_max = plt.gca().get_ylim()
    if 1 < y_max < 1.1:
        y_max = 1
    x_min, x_max = plt.gca().get_xlim()
    for i in t['enable']:
        plt.axvline(x=i, linewidth=0.7, linestyle='--', c='red')
        plt.text(i + 0.015 * (x_max - x_min), 0.985 * y_max, trigger_name + ' start', {'ha': 'left', 'va': 'top'}, rotation=90, fontsize=7)
    for i in t['disable']:
        plt.axvline(x=i, linewidth=0.7, linestyle='--', c='green')
        plt.text(i + 0.015 * (x_max - x_min), 0.985 * y_max, trigger_name + ' end', {'ha': 'left', 'va': 'top'}, rotation=90, fontsize=7)


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
    __plot_trigger(results, 'Social distancing')
    plt.show()

    plt.plot(range(len(results[PersonState.Healthy])), results['average_new_cases'], color='firebrick', linewidth=3, label='Average new cases over last 7 days')
    plt.plot(range(len(results[PersonState.Healthy])), results['new_cases'], color='lightcoral', alpha=0.5, linewidth=1, label='New cases')
    plt.legend(loc='upper right')
    plt.xlabel('Days')
    plt.ylabel('New cases in percentage of total population')
    __plot_trigger(results, 'Social distancing')
    plt.show()

    plt.plot(range(len(results[PersonState.Healthy])), results['R'], color='firebrick', linewidth=3, label='R')
    plt.plot(range(len(results[PersonState.Healthy])), [1 for _ in range(len(results[PersonState.Healthy]))], color='seagreen', linestyle='--', linewidth=2, label='R = 1')
    plt.legend(loc='upper right')
    plt.xlabel('Days')
    plt.ylabel('Effective reproductive number: R')
    __plot_trigger(results, 'Social distancing')
    plt.show()
