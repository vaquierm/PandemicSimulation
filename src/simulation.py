from src.config import Config
from src.entity_network.communities import Communities
from src.entity_network.person import PersonState


class Simulation:

    def __init__(self, config: Config):
        self.current_tick = 0
        self.ticks_per_day = config.ticks_per_day
        self.communities = Communities(config)

    def start(self):
        result = {
            PersonState.Healthy: [],
            PersonState.Incubating: [],
            PersonState.Sick: [],
            PersonState.Recovered: [],
            'new_cases': [],
            'average_new_cases': []
        }

        simulation_done = False
        while not simulation_done:
            if self.current_tick % self.ticks_per_day == 0:
                print("Day", int(self.current_tick/self.ticks_per_day))
                proportions = self.communities.get_proportions()
                result[PersonState.Healthy].append(proportions[PersonState.Healthy])
                result[PersonState.Incubating].append(proportions[PersonState.Incubating])
                result[PersonState.Sick].append(proportions[PersonState.Sick])
                result[PersonState.Recovered].append(proportions[PersonState.Recovered])
                result['new_cases'].append(self.communities.new_cases / self.communities.n_people)

                average_new_cases = 0
                n = 0
                for i in range(max(0, int(self.current_tick/self.ticks_per_day) - 7), int(self.current_tick/self.ticks_per_day)):
                    n += 1
                    average_new_cases += result['new_cases'][i]
                if n != 0:
                    average_new_cases /= n
                result['average_new_cases'].append(average_new_cases)

                self.communities.new_cases = 0

                if proportions[PersonState.Incubating] + proportions[PersonState.Sick] == 0:
                    simulation_done = True

            self.communities.tick()
            self.current_tick += 1

        return result
