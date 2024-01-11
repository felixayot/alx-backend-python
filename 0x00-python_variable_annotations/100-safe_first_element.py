#!/usr/bin/env python3
"""Script for annotated function, safe_first_element."""
from typing import Sequence, Any, Union


# The types of the elements of the input are not known
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    Returns the first element of a list if the list exists, otherwise None.
    """
    if lst:
        return lst[0]
    else:
        return None
