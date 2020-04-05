# This file contains all functions to create probability distribution functions
import random
from numpy.random import choice


def multi_dist(gaussian_list: list, weights: list):
    """
    This function generates a lambda expression for a mixture of distributions
    :param gaussian_list: The list of distributions that with be present in the distribution
    :param weights: The weights of each gaussian relative to each other
    :return: Lambda expression of mixture of all input distributions
    """
    if len(gaussian_list) != len(weights):
        raise Exception("The length of the list of distributions and the list of weights should be the same")
    ws = []
    for i in range(len(weights)):
        ws.append(weights[i] / sum(weights))
        if type(lambda: 0) != type(gaussian_list[i]):
            raise Exception("All elements of the distributions list must be lambdas")
    return lambda: gaussian_list[choice(len(gaussian_list), p=ws)]()


def gaussian(mean: float, std: float):
    """
    Create a lambda expression that returns numbers fitting the gaussian parameters
    :param mean: Mean of gaussian
    :param std: Standard dev of gaussian
    :return: Lambda expression returning items of the gaussian
    """
    return lambda: random.gauss(mean, std)


def constant(v: float):
    return lambda: v


def gaussian_time_in_ticks(mean: float, std: float):
    """
    Return a lambda expression that returns a gaussian of time in ticks.
    Example: mean=5, std=1 is a stream of numbers fitting this gaussian and is never negative
    :param mean: Mean of gaussian
    :param std: Standard dev of gaussian
    :return: Lambda expression returning stream that fits the gaussian
    """
    return lambda: round(max(random.gauss(mean, std), 0))


def constant_time_in_ticks(v: float):
    return lambda: round(max(v, 0))


def gaussian_time_in_days(mean_days: float, std_days: float, ticks_per_day: int):
    """
    Return a lambda expression that returns a gaussian of time in days (translated to ticks)
    Example: mean=4, std=1 is a stream of numbers in ticks that corresponds to a mean of 5 days and std of 1 day
    :param mean_days: Mean in days
    :param std_days: Standard deviation in days
    :param ticks_per_day: Number of ticks per day
    :return: Lambda expression returning stream that fits the gaussian
    """
    return lambda: round(max(random.gauss(mean_days * ticks_per_day, std_days * ticks_per_day), 0))


def constant_time_in_days(days: float, ticks_per_day:int):
    return lambda: round(max(days * ticks_per_day, 0))


def gaussian_prob(mean_days_per_event: float, std_days_per_event: float, ticks_per_day: int):
    """
    Return a lambda expression that returns a distributions of probabilities of an event happening at any given tick
    Example: mean=10, std=2 We expect an event to occur on average every 10 days with a standard deviation of 2 days
    :param mean_days_per_event: Mean number of days for an event to happen
    :param std_days_per_event: Standard dev in days of an event occurring
    :param ticks_per_day: Number of ticks per day
    :return: Lambda expression returning stream that fits the gaussian
    """
    return lambda: min(1, max(0, random.gauss(1 / (ticks_per_day * mean_days_per_event), std_days_per_event / (
            ticks_per_day * mean_days_per_event * mean_days_per_event))))


def constant_prob(days_per_event: float, ticks_per_day: int):
    return lambda: min(1, max(0, 1 / (ticks_per_day * days_per_event)))
