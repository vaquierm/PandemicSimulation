import random


def rand_f():
    """
    :return: Random float between 0 and 1
    """
    random.random()


def rand_i(a: int, b: int):
    """
    :return: Random int between min (included) and max (excluded)
    """
    random.randint(a, b)
