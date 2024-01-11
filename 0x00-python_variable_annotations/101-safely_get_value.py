#!/usr/bin/env python3
"""Script for annotated function, safely_get_value."""
from typing import Mapping, Any, Union, TypeVar

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any, default:
                     Union[T, None] = None) -> Union[Any, T]:
    """
    Returns for a key in a given dictionary, dct,
    otherwise, returns provided default.
    """
    if key in dct:
        return dct[key]
    else:
        return default
