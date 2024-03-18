#!/usr/bin/env python3
""" Docs """
from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """ Docs """
    if lst:
        return lst[0]
    else:
        return None
