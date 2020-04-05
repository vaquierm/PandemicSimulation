# This class is used to configure triggers
# Triggers include social distancing, travel restrictions, reduced trips to public spaces


class EventTrigger:

    def __init__(self, start_percentages: list, end_percentages: list, reduction_factor_distribution: float):
        """
        Creates an instance of Event trigger
        :param start_percentages: List of percentages of population infected (active symptomatic cases) required to reach for the event to trigger
        :param end_percentages: List of percentages of population infected (active symptomatic cases) required to each to disable an event
        :param reduction_factor_distribution: Factor by which we reduce a metric when the event triggers. For example for social distancing
                                 if this number is 5, we reduce all interactions of people by a factor of 5
                                 This should be a lambda function that returns this number and take nothing as input
        """
        if len(start_percentages) != len(end_percentages) or len(start_percentages) != len(end_percentages) + 1:
            Exception("The length of trigger start must be equal to or on greater than the length of trigger end")

        for start in start_percentages:
            if start < 0 or start > 1:
                Exception("The start trigger percentages must be numbers between 0 and 1")
        for end in end_percentages:
            if end < 0 or end > 1:
                Exception("The end trigger percentages must be numbers between 0 and 1")
        self.start_percentages = start_percentages
        self.end_percentages = end_percentages
        self.reduction_factor_distribution = reduction_factor_distribution
        self.enabled = False
        self.trigger_cooldown = 3

    def enable_at(self):
        """
        :return: Gets the next infected population percentage for the event to trigger
        """
        if len(self.start_percentages) == 0:
            return 1
        if self.trigger_cooldown > 0:
            self.trigger_cooldown -= 1
            return 1
        return self.start_percentages[0]

    def disable_at(self):
        """
        :return: Gets the next infected population percentage for the event to disable
        """
        if len(self.end_percentages) == 0:
            return 0
        if self.trigger_cooldown > 0:
            self.trigger_cooldown -= 1
            return 0
        return self.end_percentages[0]

    def enable(self):
        """
        :return: Removes the next infected population percentage for the event to trigger
        """
        if len(self.start_percentages) == 0:
            raise Exception("This event cannot be triggered")
        self.enabled = True
        self.trigger_cooldown = 2
        self.start_percentages.pop(0)

    def disable(self):
        """
        :return: Removes the next infected population percentage for the event to disable
        """
        if len(self.end_percentages) == 0:
            raise Exception("This event cannot be disabled")
        self.enabled = False
        self.trigger_cooldown = 2
        self.end_percentages.pop(0)
