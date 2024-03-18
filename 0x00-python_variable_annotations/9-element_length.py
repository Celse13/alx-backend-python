#!/usr/bin/env python3
""" Docs """
from typing import Iterable, Sequence, Tuple, List


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Docs """
    return [(i, len(i)) for i in lst]
