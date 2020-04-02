# This file contains the community object
import numpy as np

from src.config import Config
from src.entity_network.person import *


class Communities:

    def __init__(self, config: Config):
        self.people = []

        community_id = 0
        for i in range(config.number_of_communities * config.people_per_communities):
            if i % config.people_per_communities == 0:
                community_id = int(i/config.people_per_communities)

            new_person = Person(person_id=i, community_id=community_id, t)

