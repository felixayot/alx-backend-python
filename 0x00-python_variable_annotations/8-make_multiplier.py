#!/usr/bin/env python3
"""Script for make_multiplier function."""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Takes a float multiplier as argument and returns a function
    that multiplies a float by multiplier.
    """
    def get_product(value):
        return multiplier * value
    return get_product
