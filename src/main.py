from src.config import Config
from src.simulation import Simulation
import src.prob_distribution as dist

if __name__ == '__main__':
    ticks_per_day = 48
    config = Config(ticks_per_day=ticks_per_day,
                    number_of_communities=3,
                    people_per_communities=100,
                    transmit_prob_distribution=dist.gaussian_prob(2, 0.3, ticks_per_day),
                    travel_prob_distribution=dist.gaussian_prob(100, 20, ticks_per_day),
                    recovery_time_distribution=dist.gaussian_time_in_days(5, 1, ticks_per_day),
                    incubation_time_distribution=dist.gaussian_time_in_days(8, 2, ticks_per_day),
                    public_place_prob_distribution=dist.gaussian_prob(2, 0.3, ticks_per_day),
                    public_place_time_distribution=dist.gaussian_time(2, 1)
                    )

    sim = Simulation(config)

    sim.start()
