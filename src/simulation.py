from src.config import Config
from src.entity_network.communities import Communities
from src.entity_network.person import PersonState


class Simulation:

    def __init__(self, config: Config):
        self.current_tick = 0
        self.ticks_per_day = config.ticks_per_day
        self.communities = Communities(config)
        self.infection_free_communities = list(range(1, config.number_of_communities))

    def start(self):
        result = {
            PersonState.Healthy: [],
            PersonState.Incubating: [],
            PersonState.Sick: [],
            PersonState.Recovered: [],
            PersonState.Quarantined: [],
            'new_cases': [],
            'average_new_cases': [],
            'Social distancing': {'enable': [], 'disable': []},
            'Travel restrictions': {'enable': [], 'disable': []},
            'Reduced public place trips': {'enable': [], 'disable': []},
            'Testing and quarantine': {'enable': [], 'disable': []},
            'First infections': []
        }

        simulation_done = False
        while not simulation_done:
            if self.current_tick % self.ticks_per_day == 0:
                proportions = self.communities.get_proportions()

                # Add today's results to the general results
                self.__update_day_results(proportions, result)

                # Reset the new cases in the community
                self.communities.new_cases = 0

                # Check if any of the triggers must be enabled
                self.__check_triggers(proportions, result, int(self.current_tick/self.ticks_per_day))

                # Check if the simulation should end
                if proportions[PersonState.Incubating] + proportions[PersonState.Sick] == 0:
                    simulation_done = True

            self.communities.tick()
            self.current_tick += 1

        result['R'] = self.__calculate_reproductive_rate()

        return result

    def __check_triggers(self, proportions, result, day):
        p_infected = proportions[PersonState.Sick] + proportions[PersonState.Quarantined]
        # Check if social distancing must be triggered
        if self.communities.social_dist_trigger is not None:
            if (not self.communities.social_dist_trigger.enabled) and p_infected > self.communities.social_dist_trigger.enable_at():
                self.communities.social_dist_trigger.enable()
                result['Social distancing']['enable'].append(day)
            elif self.communities.social_dist_trigger.enabled and p_infected < self.communities.social_dist_trigger.disable_at():
                self.communities.social_dist_trigger.disable()
                result['Social distancing']['disable'].append(day)

        # Check if travel restrictions must be triggered
        if self.communities.travel_restrictions_trigger is not None:
            if (not self.communities.travel_restrictions_trigger.enabled) and p_infected > self.communities.travel_restrictions_trigger.enable_at():
                self.communities.travel_restrictions_trigger.enable()
                result['Travel restrictions']['enable'].append(day)
            elif self.communities.travel_restrictions_trigger.enabled and p_infected < self.communities.travel_restrictions_trigger.disable_at():
                self.communities.travel_restrictions_trigger.disable()
                result['Travel restrictions']['disable'].append(day)
            # Check if a new community got infected
            infection_free = self.communities.get_infection_free_communities()
            for i in self.infection_free_communities:
                if i not in infection_free:
                    result['First infections'].append((i, day))
            self.infection_free_communities = infection_free

        # Check reduction in public place visits must be enabled
        if self.communities.reduced_public_place_trips_trigger is not None:
            if (not self.communities.reduced_public_place_trips_trigger.enabled) and p_infected > self.communities.reduced_public_place_trips_trigger.enable_at():
                self.communities.reduced_public_place_trips_trigger.enable()
                result['Reduced public place trips']['enable'].append(day)
            elif self.communities.reduced_public_place_trips_trigger.enabled and p_infected < self.communities.reduced_public_place_trips_trigger.disable_at():
                self.communities.reduced_public_place_trips_trigger.disable()
                result['Reduced public place trips']['disable'].append(day)

        # Check if testing and quarantining must be enabled
        if self.communities.testing_trigger is not None:
            if (not self.communities.testing_trigger.enabled) and p_infected > self.communities.testing_trigger.enable_at():
                self.communities.testing_trigger.enable()
                result['Testing and quarantine']['enable'].append(day)
            elif self.communities.testing_trigger.enabled and p_infected < self.communities.testing_trigger.disable_at():
                self.communities.testing_trigger.disable()
                result['Testing and quarantine']['disable'].append(day)

    def __update_day_results(self, proportions, result):
        result[PersonState.Healthy].append(proportions[PersonState.Healthy])
        result[PersonState.Incubating].append(proportions[PersonState.Incubating])
        result[PersonState.Sick].append(proportions[PersonState.Sick])
        result[PersonState.Recovered].append(proportions[PersonState.Recovered])
        result[PersonState.Quarantined].append(proportions[PersonState.Quarantined])
        result['new_cases'].append(self.communities.new_cases / self.communities.n_people)

        average_new_cases = 0
        n = 0
        for i in range(max(0, int(self.current_tick / self.ticks_per_day) - 7),
                       int(self.current_tick / self.ticks_per_day)):
            n += 1
            average_new_cases += result['new_cases'][i]
        if n != 0:
            average_new_cases /= n
        result['average_new_cases'].append(average_new_cases)

    def __calculate_reproductive_rate(self):
        total_days = int(self.current_tick / self.ticks_per_day) + 1
        groups = []
        for i in range(total_days):
            groups.append([])

        for person in self.communities.people:
            if person.sick_time < 0:
                continue
            infected_day = int((self.current_tick - person.sick_time) / self.ticks_per_day)
            for i in range(infected_day, min(len(groups), infected_day + int((person.incubation_time + person.recovery_time) / self.ticks_per_day))):
                groups[i].append(person.infection_count)

        for i in range(total_days):
            if len(groups[i]) == 0:
                groups[i] = 0
            else:
                groups[i] = sum(groups[i]) / len(groups[i])

        return groups
