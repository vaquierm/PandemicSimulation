# This file contains the community object
import random

from src.config import Config
from src.entity_network.person import *


def random_travel_table(travel_prob, n_communities: int):
    return np.random.uniform(size=n_communities) * travel_prob / n_communities


class Communities:

    def __init__(self, config: Config):
        """
        Create the communities based on the configuration object
        :param config: Configuration of the simulation
        """
        self.people = []

        n_people = config.number_of_communities * config.people_per_communities

        # Create the person objects that represents our total population
        for i in range(n_people):
            community_id = int(i/config.people_per_communities)

            travel_table = random_travel_table(config.travel_prob_distribution(), config.number_of_communities)

            new_person = Person(
                person_id=i,
                community_id=community_id,
                travel_table=travel_table,
                public_place_probability=config.public_place_prob_distribution(),
                transmit_probability=config.travel_prob_distribution(),
                recovery_time=config.recovery_time_distribution(),
                incubation_time=config.incubation_time_distribution()
            )

            self.people.append(new_person)

        self.public_place_time_dist = config.public_place_time_distribution

        # Create the matrix of interactions
        self.interaction_matrix = np.random.uniform(low=0, high=1/n_people, size=(n_people, n_people))

        self.ticks_per_day = config.ticks_per_day

    def tick(self):
        """
        Runs the simulation for one tick
        """
        for i in range(len(self.people)):
            person = self.people[i]

            # First see if the person needs to travel
            if person.place == PersonPlace.Regular and random.random() < person.travel_probability:
                person.set_place(PersonPlace.TravelHub, round(self.ticks_per_day / 12))
                person.travel_source = True

            # Then check if the person is done being at the airport
            if person.place == PersonPlace.TravelHub and person.time_in_place_remaining <= 0:
                # Check if the person spent over two hours in the source airport
                if person.travel_source:
                    person.travel_source = False
                    person.community_id = person.travel()
                    person.time_in_place_remaining = round(self.ticks_per_day / 24)
                # Check if the person spent over one hour in the destination airport
                elif (not person.travel_source) and person.time_in_place_remaining <= 0:
                    person.set_place(PersonPlace.Regular)

            # The check if the person needs to go to the public place
            if person.place == PersonPlace.Regular and random.random() < person.public_place_probability:
                person.set_place(PersonPlace.PublicSpace, self.public_place_time_dist())

            # Check if anyone is coming out of the grocery store
            if person.place == PersonPlace.PublicSpace and person.time_in_place_remaining <= 0:
                person.set_place(PersonPlace.Regular)

            # Advance the simulation by one tick for the person
            person.tick()

    def get_proportions(self):
        """
        :return: Dictionary with number of people from each state. (Healthy, Sick, Recovered)
        """
        prop = {
            PersonState.Healthy: 0,
            PersonState.Incubating: 0,
            PersonState.Sick: 0,
            PersonState.Recovered: 0
        }
        for person in self.people:
            prop[person.get_state()] += 1

        return prop
