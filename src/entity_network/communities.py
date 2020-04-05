# This file contains the community object
import networkx as nx

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

        self.n_people = config.number_of_communities * config.people_per_communities
        self.n_communities = config.number_of_communities

        # Create the person objects that represents our total population
        for i in range(self.n_people):
            community_id = int(i/config.people_per_communities)

            travel_table = random_travel_table(config.travel_prob_distribution(), config.number_of_communities)

            new_person = Person(
                person_id=i,
                community_id=community_id,
                travel_table=travel_table,
                public_place_probability=config.public_place_prob_distribution(),
                transmit_probability=config.transmit_prob_distribution(),
                recovery_time=config.recovery_time_distribution(),
                incubation_time=config.incubation_time_distribution()
            )

            # Infect people in community 0 so that 2% of the total population is infected
            if community_id == 0:
                if i == 0:
                    new_person.infect()
                infected_p = 2 * self.n_communities / self.n_people
                if random.random() < infected_p:
                    new_person.infect()

            self.people.append(new_person)

        self.public_place_time_dist = config.public_place_time_distribution

        # Create the matrix of interactions
        self.interaction_matrix = np.random.uniform(low=0, high=1/self.n_people, size=(self.n_people, self.n_people))

        # Number op people someone closely interacts with
        close_interactions = 17
        try:
            graph = nx.connected_watts_strogatz_graph(self.n_people, close_interactions, 0.3)
        except:
            raise Exception("Something went wrong when creating the network of people, try again...")
        self.interaction_matrix = nx.adjacency_matrix(graph).toarray().astype('float')

        interaction_mean = config.number_of_communities / (self.n_people - 1)

        # Proportions of close interactions and non close interactions
        prop_close = close_interactions / self.n_people

        mu_0 = 1 / (3 * prop_close + 1) * interaction_mean / 2
        mu_1 = 4 * mu_0

        self.interaction_matrix[self.interaction_matrix == 0] = np.random.normal(mu_0, mu_0/10, size=self.interaction_matrix[self.interaction_matrix == 0].shape)
        self.interaction_matrix[self.interaction_matrix == 1] = np.random.normal(mu_1, mu_1/10, size=self.interaction_matrix[self.interaction_matrix == 1].shape)
        self.interaction_matrix[self.interaction_matrix < 0] = 0

        self.interaction_matrix = np.tril(self.interaction_matrix, -1)

        # Create an alternate social distancing interaction matrix
        distancing_factor_matrix = np.zeros(self.interaction_matrix.shape)
        for i in range(self.n_people):
            dist_factor_i = config.social_distancing_trigger.reduction_factor_distribution()
            distancing_factor_matrix[i, :] = dist_factor_i
        distancing_factor_matrix = (distancing_factor_matrix + distancing_factor_matrix.T) / 2

        self.social_dist_interaction_matrix = self.interaction_matrix / distancing_factor_matrix

        # Define the trigger used for social distancing
        self.social_dist_trigger = config.social_distancing_trigger

        self.ticks_per_day = config.ticks_per_day
        self.new_cases = 0

    def tick(self):
        """
        Runs the simulation for one tick
        """
        # Keep count of people in public places and travel hubs
        counts = {}
        for i in range(self.n_communities):
            counts[i] = {
                PersonPlace.TravelHub: [],
                PersonPlace.PublicSpace: []
            }

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

            if person.place == PersonPlace.PublicSpace or person.place == PersonPlace.TravelHub:
                counts[person.community_id][person.place].append(person.id)

        # Now the infecting. We want only people in the same community infecting each other
        # Furthermore within the same community, we only want people in the same public space or travel hub

        # First make a copy of the infection matrix
        if self.social_dist_trigger.enabled:
            interactions = self.social_dist_interaction_matrix.copy()
        else:
            interactions = self.interaction_matrix.copy()

        # Scale the rows and columns for public places and travel
        for i in range(self.n_communities):
            public_space_count = len(counts[i][PersonPlace.PublicSpace])
            if public_space_count > 1:
                arr = np.array(counts[i][PersonPlace.PublicSpace])
                ind = np.array(np.meshgrid(arr, arr)).T.reshape(-1)
                interactions[ind[0:][::2], ind[1:][::2]] *= 2 * self.n_people / (public_space_count - 1) / self.n_communities
            travel_hub_count = len(counts[i][PersonPlace.TravelHub])
            if travel_hub_count > 1:
                arr = np.array(counts[i][PersonPlace.TravelHub])
                ind = np.array(np.meshgrid(arr, arr)).T.reshape(-1)
                interactions[ind[0:][::2], ind[1:][::2]] *= 2 * self.n_people / (travel_hub_count - 1) / self.n_communities

        # Determine what interactions happen
        interactions_happen = np.random.uniform(low=0, high=1, size=interactions.shape)

        interactions[interactions_happen > interactions] = 0

        index_i, index_j = np.nonzero(interactions)

        del interactions_happen, interactions

        # Now that we have the indexes, determine infections
        for i in range(index_i.shape[0]):
            p_i = self.people[index_i[i]]
            p_j = self.people[index_j[i]]
            if p_i.community_id != p_j.community_id or p_i.place != p_j.place:
                continue
            if p_i.get_state() == PersonState.Recovered or p_j.get_state() == PersonState.Recovered:
                continue
            if p_i.get_state() == p_j.get_state():
                continue
            # If person i is healthy and person j isn't, there could be an infection
            if (p_i.get_state() == PersonState.Healthy) and (p_j.get_state() == PersonState.Incubating or p_j.get_state() == PersonState.Sick):
                transmit_prob = (p_i.transmit_prob + p_j.transmit_prob) / 2
                if p_j.place != PersonPlace.Regular:
                    transmit_prob *= 5
                if random.random() < transmit_prob:
                    p_i.infect()
                    p_j.infection_count += 1
                    self.new_cases += 1
            # If person j is healthy and person i isn't, there could be an infection
            elif (p_j.get_state() == PersonState.Healthy) and (p_i.get_state() == PersonState.Incubating or p_i.get_state() == PersonState.Sick):
                transmit_prob = (p_i.transmit_prob + p_j.transmit_prob) / 2
                if p_j.place != PersonPlace.Regular:
                    transmit_prob *= 5
                if random.random() < transmit_prob:
                    p_j.infect()
                    p_i.infection_count += 1
                    self.new_cases += 1

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

        prop[PersonState.Healthy] /= self.n_people
        prop[PersonState.Sick] /= self.n_people
        prop[PersonState.Incubating] /= self.n_people
        prop[PersonState.Recovered] /= self.n_people

        return prop
