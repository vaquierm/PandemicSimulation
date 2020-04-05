# This file contains the Simulation configuration class which contains all data to start a simulation
from src.triggers.trigger import EventTrigger


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
                 public_place_time_distribution,
                 social_distancing_trigger: EventTrigger = None,
                 ):
        if ticks_per_day <= 0:
            raise Exception("There must be at least 1 tick per day")
        self.ticks_per_day = ticks_per_day
        if number_of_communities <= 0:
            raise Exception("The number of communities must be at least 1")
        if number_of_communities * people_per_communities < 200:
            raise Exception("The simulation must run with more than 200 people.")
        self.number_of_communities = number_of_communities
        self.people_per_communities = people_per_communities

        # Distributions
        if type(lambda: 0) != type(transmit_prob_distribution):
            raise Exception("The transmit prob distribution must be a lambda")
        self.transmit_prob_distribution = transmit_prob_distribution
        if type(lambda: 0) != type(travel_prob_distribution):
            raise Exception("The travel prob distribution must be a lambda")
        self.travel_prob_distribution = travel_prob_distribution
        if type(lambda: 0) != type(recovery_time_distribution):
            raise Exception("The recovery time distribution must be a lambda")
        self.recovery_time_distribution = recovery_time_distribution
        if type(lambda: 0) != type(incubation_time_distribution):
            raise Exception("The incubation time distribution must be a lambda")
        self.incubation_time_distribution = incubation_time_distribution
        if type(lambda: 0) != type(public_place_prob_distribution):
            raise Exception("The public place prob distribution must be a lambda")
        self.public_place_prob_distribution = public_place_prob_distribution
        if type(lambda: 0) != type(public_place_time_distribution):
            raise Exception("The public place time distribution must be a lambda")
        self.public_place_time_distribution = public_place_time_distribution

        # Triggers
        self.social_distancing_trigger = social_distancing_trigger
