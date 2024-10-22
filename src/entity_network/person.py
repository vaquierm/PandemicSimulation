# This file contains the person entity that contains the state of an individual
# in the population.
import enum
import numpy as np
import random

from src.triggers.testing_trigger import TestingTrigger


class PersonState(enum.Enum):
    # Indicates the health state of the person
    Healthy = 0
    Incubating = 1
    Sick = 2
    Recovered = 3
    # Quarantined after testing positive (No more interactions with anyone until recovered)
    Quarantined = 4


class PersonPlace(enum.Enum):
    # Indicates where in the community the person is
    # Regular place
    Regular = 0
    # At a public space such as grocery store
    PublicSpace = 1
    # At a travel hub such as an airport
    TravelHub = 2


class Person:

    def __init__(self, person_id: int, community_id: int, travel_table: np.ndarray, public_place_probability: float,
                 transmit_probability: float, recovery_time: int, incubation_time: int, travel_reduction_factor: float,
                 reduced_public_place_trips_factor: float, time_to_test: int, testing_trigger: TestingTrigger):
        """
        Creates an instance of a person
        :param person_id: ID of the person
        :param community_id: The ID of the community the person currently is in
        :param travel_table: The proportion of which community the person is likely to travel to (The sum equals their probability to travel on a given tick)
        :param public_place_probability: The probability that the person will go to the grocery store at a given simulation tick
        :param transmit_probability: The probability that they have of transmitting or receiving the virus when interacting with someone
        :param recovery_time: Time in simulation ticks to recover after showing symptoms
        :param incubation_time: Time in simulation ticks for incubation period
        :param travel_reduction_factor: Factor by which this person reduces their travel if a travel restriction is put in place
        :param reduced_public_place_trips_factor: Factor by which the person reduces their trips to public places
        :param time_to_test: Time in ticks that need to pass for the person to get tested and go into quarantine
        :param testing_trigger: Trigger indicating if testing and quarantine is happening or not
        """
        self.id = person_id
        self.community_id = community_id
        self.travel_table = travel_table
        self.travel_probability = travel_table.sum()
        self.public_place_probability = public_place_probability
        self.sick_time = -1
        self.transmit_prob = transmit_probability
        self.recovery_time = recovery_time
        self.incubation_time = incubation_time
        self.place = PersonPlace.Regular
        self.time_in_place_remaining = -1
        self.travel_source = False
        self.infection_count = 0
        self.travel_reduction_factor = travel_reduction_factor
        self.reduced_public_place_trips_factor = reduced_public_place_trips_factor
        self.time_to_test = time_to_test
        self.testing_trigger = testing_trigger

    def tick(self):
        """
        Advance the simulation for this person by one tick
        """
        if self.sick_time >= 0:
            self.sick_time += 1

        if self.time_in_place_remaining >= 0:
            self.time_in_place_remaining -= 1

    def get_state(self):
        """
        Gets the infection state of the person
        :return: PersonState of this person
        """
        if self.sick_time > self.recovery_time + self.incubation_time:
            return PersonState.Recovered
        elif (self.testing_trigger is not None) and self.testing_trigger.enabled and self.time_to_test >= 0 and self.sick_time > self.incubation_time + self.time_to_test:
            return PersonState.Quarantined
        elif self.sick_time > self.incubation_time:
            return PersonState.Sick
        elif self.sick_time >= 0:
            return PersonState.Incubating
        else:
            return PersonState.Healthy

    def set_place(self, new_place: PersonPlace, time_in_place_remaining: int = -1):
        """
        Set the place state of the person
        :param new_place: New place state
        :param time_in_place_remaining: Time remaining in this place
        """
        if self.place == new_place:
            raise Exception("The person is already in place: " + str(self.place))

        self.time_in_place_remaining = time_in_place_remaining
        self.place = new_place

    def infect(self):
        """
        Infects the person. If they have already been infected in the past, then an exception in raised
        """
        # Check if the person can be infected
        if self.get_state() != PersonState.Healthy:
            raise Exception("Cannot infect a person that is in state: " + str(self.get_state()))

        # Set the sick tick counter to 0
        self.sick_time = 0

    def travel(self):
        """
        Chose a community at random to travel to
        :return: Community id to travel to
        """
        weights = self.travel_table.copy()

        for i in range(weights.shape[0]):
            weights[i] *= random.random()

        # If the community to travel to is the community the person already is in, set that weight to -1
        if weights.argmax() == self.community_id:
            weights[weights.argmax()] = -1

        return weights.argmax()
