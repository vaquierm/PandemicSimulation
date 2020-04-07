# This file contains the functions to visualize the simulation results
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np

from src.entity_network.person import PersonState


def __plot_trigger(results, trigger_name: str):
    t = results[trigger_name]
    _, y_max = plt.gca().get_ylim()
    if 1 < y_max < 1.1:
        y_max = 1
    x_min, x_max = plt.gca().get_xlim()
    for x in t['enable']:
        plt.axvline(x=x, linewidth=0.7, linestyle='--', c='red')
        plt.text(x + 0.015 * (x_max - x_min), 0.985 * y_max, trigger_name + ' start', {'ha': 'left', 'va': 'top'}, rotation=90, fontsize=7)
    for x in t['disable']:
        plt.axvline(x=x, linewidth=0.7, linestyle='--', c='green')
        plt.text(x + 0.015 * (x_max - x_min), 0.985 * y_max, trigger_name + ' end', {'ha': 'left', 'va': 'top'}, rotation=90, fontsize=7)


def __plot_all_triggers(results):
    __plot_trigger(results, 'Social distancing')
    __plot_trigger(results, 'Travel restrictions')
    __plot_trigger(results, 'Reduced public place trips')
    __plot_trigger(results, 'Testing and quarantine')
    _, y_max = plt.gca().get_ylim()
    if 1 < y_max < 1.1:
        y_max = 1
    x_min, x_max = plt.gca().get_xlim()
    for i, x in results['First infections']:
        plt.axvline(x=x, linewidth=0.7, linestyle='--', c='slategray')
        plt.text(x + 0.015 * (x_max - x_min), 0.985 * y_max, 'First infection in community ' + str(i), {'ha': 'left', 'va': 'top'}, rotation=90, fontsize=7)


def plot_simulation_results(results: dict):
    """
    Plot the results of the simulation
    :param results: Simulation results dictionary returned by the start method of the simulation
    """
    data = [results[PersonState.Sick], results[PersonState.Incubating], results[PersonState.Healthy], results[PersonState.Recovered]]
    labels = ['Symptomatic', 'Asymptomatic', 'Healthy', 'Recovered']
    colors = ['firebrick', 'darkorange', 'steelblue', 'darkgrey']

    if sum(results[PersonState.Quarantined]) > 0:
        data.insert(0, results[PersonState.Quarantined])
        labels.insert(0, 'Quarantined')
        colors.insert(0, 'lightpink')

    plt.stackplot(range(len(results[PersonState.Healthy])), data,
                  labels=labels,
                  alpha=0.8, colors=colors)
    plt.legend(loc='upper right')
    plt.xlabel('Days')
    plt.ylabel('Percentage of population')
    __plot_all_triggers(results)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.show()

    plt.plot(range(len(results[PersonState.Healthy])), results['average_new_cases'], color='firebrick', linewidth=3, label='Average new cases over last 7 days')
    plt.plot(range(len(results[PersonState.Healthy])), results['new_cases'], color='lightcoral', alpha=0.5, linewidth=1, label='New cases')
    plt.legend(loc='upper right')
    plt.xlabel('Days')
    plt.ylabel('New cases in percentage of total population')
    __plot_all_triggers(results)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.show()

    plt.plot(range(len(results[PersonState.Healthy])), results['R'], color='firebrick', linewidth=3, label='R')
    plt.plot(range(len(results[PersonState.Healthy])), [1 for _ in range(len(results[PersonState.Healthy]))], color='seagreen', linestyle='--', linewidth=2, label='R = 1')
    plt.legend(loc='upper right')
    plt.xlabel('Days')
    plt.ylabel('Effective reproductive number: R')
    __plot_all_triggers(results)
    plt.show()


def plot_distribution(dist, metric, bins=20):
    N = 5000
    arr = np.array([dist() for _ in range(N)])
    plt.hist(arr, bins=bins, weights=np.ones(N) / N, color='steelblue')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.ylabel('Percentage of total population')
    plt.xlabel(metric)
    plt.title('Proportions of ' + metric)
    plt.show()

