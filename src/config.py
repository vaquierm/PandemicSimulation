# This file contains the Simulation configuration class which contains all data to start a simulation


class Config:

    def __init__(self,
                 ticks_per_day: float,
                 number_of_communities: int,
                 people_per_communities: int,
                 transmit_prob_distribution,
                 travel_prob_distribution,
                 recovery_time_distribution,
                 incubation_time_distribution,
                 public_place_prob_distribution,
                 public_place_time_distribution
                 ):
        self.ticks_per_day = ticks_per_day
        self.number_of_communities = number_of_communities
        self.people_per_communities = people_per_communities
        self.transmit_prob_distribution = transmit_prob_distribution
        self.travel_prob_distribution = travel_prob_distribution
        self.recovery_time_distribution = recovery_time_distribution
        self.incubation_time_distribution = incubation_time_distribution
        self.public_place_prob_distribution = public_place_prob_distribution
        self.public_place_time_distribution = public_place_time_distribution
