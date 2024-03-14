#!/usr/bin/env python3
""" Docs """
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """ Maka a multiplier """

    def mult(m: float) -> float:
        """ Mult """
        return m * multiplier

    return mult
