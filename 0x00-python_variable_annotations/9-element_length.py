#!/usr/bin/env python3
"""Script for annotated function, element_length."""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Returns the length of each element in a list of iterable sequence elements.
    """
    return [(i, len(i)) for i in lst]
