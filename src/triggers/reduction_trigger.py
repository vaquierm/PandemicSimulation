from src.triggers.trigger import EventTrigger


class ReductionEventTrigger(EventTrigger):

    def __init__(self, start_percentages: list, end_percentages: list, reduction_factor_distribution):
        """
        Creates an instance of Reduction Event trigger
        :param start_percentages: List of percentages of population infected (active symptomatic cases) required to reach for the event to trigger
        :param end_percentages: List of percentages of population infected (active symptomatic cases) required to each to disable an event
        :param reduction_factor_distribution: Factor by which we reduce a metric when the event triggers. For example for social distancing
                                 if this number is 5, we reduce all interactions of people by a factor of 5
                                 This should be a lambda function that returns this number and take nothing as input
        """
        super().__init__(start_percentages, end_percentages)
        self.reduction_factor_distribution = reduction_factor_distribution
        if type(lambda: 0) != type(reduction_factor_distribution):
            raise Exception("The reduction factor distribution must be a lambda")
