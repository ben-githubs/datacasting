from dataclasses import dataclass
from datetime import datetime
import typing

from datacasting import to_dataclass


@dataclass
class Class1:
    foo: str
    bar: int
    biz: float
    baz: bool

def test_simple():
    values = {
        'foo': 'string',
        'bar': 0,
        'biz': 0.1,
        'baz': True
    }
    control = Class1(**values)
    result = to_dataclass(Class1, values)
    # We do value-wise comparison, since we have to compare floats differently
    assert control.foo == result.foo
    assert control.bar == result.bar
    assert isinstance(result.biz, float)
    assert (control.biz - result.biz) ** 2 < 0.015
    assert control.baz == result.baz

@dataclass
class Class2:
    foo: str
    bar: int = 2

def test_optional_1():
    values = {
        'foo': 10,
        'bar': 10
    }
    control = Class2(foo="10", bar=10)
    result = to_dataclass(Class2, values)
    assert control == result

def test_optional_2():
    values = {
        'foo': 10
    }
    control = Class2(foo="10")
    result = to_dataclass(Class2, values)
    assert control == result

@dataclass
class Class3:
    foo: int
    bar: typing.List[int]
    baz: typing.Union[int, str]

def test_union_1():
    values = {
        'foo': 1,
        'bar': [1, 2, 3],
        'baz': 10
    }
    control = Class3(foo=1, bar=[1,2,3], baz=10)
    result = to_dataclass(Class3, values)
    assert control == result

def test_union_2():
    values = {
        'foo': 1,
        'bar': [1, 2, 3],
        'baz': [12]
    }
    control = Class3(foo=1, bar=[1,2,3], baz='[12]')
    result = to_dataclass(Class3, values)
    assert control == result

@dataclass
class Class4:
    foo: Class2
    bar: bool

def test_nesting():
    values = {
        'foo': {
            'foo': 10,
            'bar': 10
        },
        'bar': False
    }
    control = Class4(
        foo = Class2('10', 10),
        bar = False
    )
    result = to_dataclass(Class4, values)
    assert control == result

@dataclass
class Class5:
    foo: datetime

def test_hook_datetime():
    hooks = {
        datetime: datetime.fromisoformat
    }
    values = {
        'foo': '2023-10-11T00:00:00'
    }
    control = Class5(foo=datetime(2023,10,11,0,0,0))
    result = to_dataclass(Class5, values, hooks)
    assert control == result

@dataclass
class Class6:
    foo: typing.Union[str, int]

def test_union_override():
    values = {
        'foo': 10
    }
    result = to_dataclass(Class6, values)
    assert isinstance(result.foo, int)