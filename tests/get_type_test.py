from dataclasses import dataclass
from typing import List, Tuple, Dict, Set, Optional, Sequence

from datacasting import to_dataclass
from datacasting._util import get_types

@dataclass
class SimpleClass:
    my_int: int
    my_float: float
    my_str: str

@dataclass
class SequenceClass:
    my_list_str: List[str]
    my_list_int: List[int]
    my_tuple: Tuple[int, int, str]
    my_dict: Dict[str, int]
    my_set: Set[int]
    my_sequence: Sequence[int]

@dataclass
class OptionalClass:
    option_int: Optional[int]
    option_str: Optional[str]
    option_list: Optional[List[float]]

def test_types_simple():
    types = get_types(SimpleClass)
    assert types == {
        'my_int': int,
        'my_float': float,
        'my_str': str
    }

def test_get_types_sequence():
    types = get_types(SequenceClass)
    assert types == {
        'my_list_str': list,
        'my_list_int': list,
        'my_tuple': tuple,
        'my_dict': dict,
        'my_set': set,
        'my_sequence': list
    }

def test_get_types_optional():
    types = get_types(OptionalClass)
    assert types == {
        'option_int': int,
        'option_str': str,
        'option_list': list
    }