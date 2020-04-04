from src.config import Config
from src.entity_network.communities import Communities
from src.entity_network.person import PersonState


class Simulation:

    def __init__(self, config: Config):
        self.current_tick = 0
        self.ticks_per_day = config.ticks_per_day
        self.communities = Communities(config)

    def start(self):
        result = []

        simulation_done = False
        while not simulation_done:
            if self.current_tick % self.ticks_per_day == 0:
                print("Day", self.current_tick/self.ticks_per_day)
                proportions = self.communities.get_proportions()
                result.append(proportions)

                if proportions[PersonState.Incubating] + proportions[PersonState.Sick] == 1:
                    simulation_done = True

            self.communities.tick()
            self.current_tick += 1


