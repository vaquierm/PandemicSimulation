from src.triggers.trigger import EventTrigger


class TestingTrigger(EventTrigger):

    def __init__(self, start_percentages: list, end_percentages: list, time_to_test_distribution, unsuccessful_test_prob_distribution):
        """
        Creates an instance of Reduction Event trigger
        :param start_percentages: List of percentages of population infected (active symptomatic cases) required to reach for the event to trigger
        :param end_percentages: List of percentages of population infected (active symptomatic cases) required to each to disable an event
        :param time_to_test_distribution: Lambda expression generating numbers for
                                          time since starting to show symptoms that people get tested
                                          and go into quarantine
        :param unsuccessful_test_prob_distribution: Lambda expression generating number for
                                                    the probability of a test being unsuccessful.
                                                    (Test fails, or person doesnt quarantine)
        """
        super().__init__(start_percentages, end_percentages)
        self.time_to_test_distribution = time_to_test_distribution
        if type(lambda: 0) != type(time_to_test_distribution):
            raise Exception("The time to test distribution must be a lambda")
        self.unsuccessful_test_prob_distribution = unsuccessful_test_prob_distribution
        if type(lambda: 0) != type(unsuccessful_test_prob_distribution):
            raise Exception("The unsuccessful test prob distribution must be a lambda")
