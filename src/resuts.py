# This file contains the logic that processes the results and display more information
from src.entity_network.person import PersonState


def print_result_summary(sim_results):
    days = len(sim_results[PersonState.Incubating])

    # Get the final percentage of population that got the infection
    final_healthy = sim_results[PersonState.Healthy][days - 1]
    print('(' + format(final_healthy * 100, '.2f') + '%) The percentage of people that did not get infected')
    print('(' + format((1 - final_healthy) * 100, '.2f') + '%) The percentage of people that did get infected')

    # Find the peak number of infected people
    peak_infections = 0
    peak_infections_day = 0
    for i in range(days):
        infections_i = sim_results[PersonState.Sick][i] + sim_results[PersonState.Quarantined][i]
        if infections_i > peak_infections:
            peak_infections = infections_i
            peak_infections_day = i
    print('Day ' + str(peak_infections_day) + ': (' + format(peak_infections * 100, '.2f') + '%) The peak percentage of total sick people (Quarantine included)')

    # Get the peak number of infectious people
    peak_infections = 0
    peak_infections_day = 0
    for i in range(days):
        infections_i = sim_results[PersonState.Sick][i] + sim_results[PersonState.Incubating][i]
        if infections_i > peak_infections:
            peak_infections = infections_i
            peak_infections_day = i
    print('Day ' + str(peak_infections_day) + ': (' + format(peak_infections * 100, '.2f') + '%) The peak percentage of total infectious people (Quarantine not included)')

    # Find the highest number of new cases
    max_new_cases = 0
    max_new_cases_day = 0
    for i in range(days):
        if sim_results['average_new_cases'][i] > max_new_cases:
            max_new_cases = sim_results['average_new_cases'][i]
            max_new_cases_day = i
    print('Day ' + str(max_new_cases_day) + ': (' + format(max_new_cases * 100, '.2f') + '%) The peak percentage of total population as average daily new cases')
