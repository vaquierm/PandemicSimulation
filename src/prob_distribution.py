# This file contains all functions to create probability distribution functions
import random


def gaussian(mean: float, std: float):
    return lambda: random.gauss(mean, std)


def gaussian_time_in_ticks(mean: float, std: float):
    return lambda: round(max(random.gauss(mean, std), 0))


def gaussian_time_in_days(mean_days: float, std_days: float, ticks_per_day: int):
    return lambda: round(max(random.gauss(mean_days * ticks_per_day, std_days * ticks_per_day), 0))


def gaussian_prob(mean_days_per_event: float, std_days_per_event: float, ticks_per_day: int):
    return lambda: min(1, max(0, random.gauss(1/(ticks_per_day * mean_days_per_event), std_days_per_event/(ticks_per_day * mean_days_per_event * mean_days_per_event))))
