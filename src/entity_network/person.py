# This file contains the person entity that contains the state of an individual
# in the population.
import enum
import numpy as np
import random


class PersonState(enum.Enum):
    # Indicates the health state of the person
    Healthy = 0
    Incubating = 1
    Sick = 2
    Recovered = 3


class PersonPlace(enum.Enum):
    # Indicates where in the community the person is
    # Regular place
    Regular = 0
    # At a public space such as grocery store
    PublicSpace = 1
    # At a travel hub such as an airport
    TravelHub = 2


class Person:

    def __init__(self, person_id: int, community_id: int, travel_table: np.ndarray, transmit_probability: float, recovery_time: int, incubation_time: int):
        """
        Creates an instance of a person
        :param person_id: ID of the person
        :param community_id: The ID of the community the person currently is in
        :param travel_table: The proportion of which community the person is likely to travel to (The sum equals their probability to travel on a given tick)
        :param transmit_probability: The probability that they have of transmitting or receiving the virus
        :param recovery_time: Time in simulation ticks to recover after showing symptoms
        :param incubation_time: Time in simulation ticks for incubation period
        """
        self.id = person_id
        self.community_id = community_id
        self.travel_table = travel_table
        self.travel_probability = travel_table.sum()
        self.__sick_time = -1
        self.transmit_prob = transmit_probability
        self.recovery_time = recovery_time
        self.incubation_time = incubation_time
        self.place = PersonPlace.Regular
        self.time_in_place = 0

    def tick(self):
        """
        Advance the simulation for this person by one tick
        """
        if self.__sick_time >= 0:
            self.__sick_time += 1

        self.time_in_place += 1

    def get_state(self):
        """
        Gets the infection state of the person
        :return: PersonState of this person
        """
        if self.__sick_time > self.recovery_time + self.incubation_time:
            return PersonState.Recovered
        elif self.__sick_time > self.incubation_time:
            return PersonState.Sick
        elif self.__sick_time >= 0:
            return PersonState.Incubating
        else:
            return PersonState.Healthy

    def set_place(self, new_place: PersonPlace.value):
        if self.place == new_place:
            raise Exception("The person is already in place: " + str(self.place))

        self.place = new_place
        self.time_in_place = 0

    def infect(self):
        """
        Infects the person. If they have already been infected in the past, then an exception in raised
        """
        # Check if the person can be infected
        if self.get_state() != PersonState.Healthy:
            raise Exception("Cannot infect a person that is in state: " + str(self.get_state()))

        # Set the sick tick counter to 0
        self.__sick_time = 0

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

