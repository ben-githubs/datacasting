""" utility functions for 'datacasting'; not inteded to be called outside of this package.
"""
from collections.abc import Sequence
from dataclasses import fields
import typing

""" Returns the base type to use for casting from aliases like List, Tuple, Optional, etc.
"""
def get_types(class_):
    types = dict()
    for f in fields(class_):
        types[f.name] = get_type(f.type)
    return types

""" Returns the base type for a single object
"""
def get_type(type_):
    if hasattr(type_, '__origin__'):
        # Special Case: Union and Optional (recall: Optional[x] = Union[x, None])
        if type_.__origin__ == typing.Union:
            types = [get_type(arg) for arg in type_.__args__ if arg != type(None)]
            if len(types) == 1: # When we use Optional
                return types[0]
            return types # When we use Union
        elif type_.__origin__ == Sequence:
            return list # Default all sequences to list
        return type_.__origin__
    return type_