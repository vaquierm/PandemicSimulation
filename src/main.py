from src.config import Config
from src.simulation import Simulation
import src.prob_distribution as dist
from src.visualization import plot_simulation_results
from src.triggers.reduction_trigger import ReductionEventTrigger

if __name__ == '__main__':
    ticks_per_day = 48
    config = Config(ticks_per_day=ticks_per_day,
                    number_of_communities=3,
                    people_per_communities=100,
                    transmit_prob_distribution=dist.gaussian_prob(8, 1, ticks_per_day),
                    travel_prob_distribution=dist.gaussian_prob(40, 2, ticks_per_day),
                    recovery_time_distribution=dist.gaussian_time_in_days(14, 3, ticks_per_day),
                    incubation_time_distribution=dist.gaussian_time_in_days(11, 3, ticks_per_day),
                    public_place_prob_distribution=dist.gaussian_prob(4, 1, ticks_per_day),
                    public_place_time_distribution=dist.gaussian_time_in_ticks(1, 0.2),
                    social_distancing_trigger=None,#EventTrigger([0.1], [0.05], dist.gaussian(5, 1)),
                    reduced_public_place_trips_trigger=None#EventTrigger([0.05], [], dist.multi_dist([dist.gaussian(5, 1), dist.constant(5)], [0.8, 0.2]))
                    )

    sim = Simulation(config)

    # Run the simulation
    sim_results = sim.start()

    # Plot the results
    plot_simulation_results(results=sim_results)
