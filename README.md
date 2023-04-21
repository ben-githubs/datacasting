# DataCasting
The datacasting package intends to make it easy to instantiate dataclasses. It is often useful to convert dictionaries to dataclasses, but before doing so, some data formats need to be cast. Common examples are strings to datetimes, and nested dictionaries to other dataclasses. This package automates the casting process for several common types, and allows for extensibility to add casting functions for other types as well.

## Usage
### Basic Usage
The simplest use case is converting a single-level dictionary with built-in data types:
```
from dataclasses import dataclasses
from datacasting import to_dataclass

@dataclass
class Person:
    name: str
    age: int

my_vars = {
    'name': 'Cotton-Eye Joe',
    'age': 98
}

person = to_dataclass(Person, my_vars)
```

Obviouslty, for simple cases like this, `datacasting` offers no advantages over simply calling `person = Person(**my_vars)`. However, it quickly becomes useful for more complicated cases.

### Nested Dataclasses
When you want to instantiate a dataclass that has another dataclass as one of it's attributes, you'd normally need to ensure the inner dataclass is properly instantiated before you can instantate the outer one. With `datacasting`, that task is automated for you.
```
from dataclasses import dataclasses
from datacasting import to_dataclass

@dataclass
class Song:
    title: str
    author: str
    release_year: int

@dataclass
class Person:
    name: str
    age: int
    favourite_song: Song

my_vars = {
    'name': 'Cotton-Eye Joe',
    'age': 98,
    'favourite_song': {
        'title': 'If it hadn't been for Cotton-Eye Joe',
        'author': 'Rednex'
        'release_year': 1995
    }
}

person = to_dataclass(Person, my_vars)
```

In this example, `to_dataclass` will automatically detect that the field `favourite_song` should be of type `Song`, which is another dataclass. It then calls `to_dataclass` on the inner dictionary.

### Non-Trivial Data Types
For most data types, you can perform a simple cast: for example, `my_str = str(my_var)` will correctly cast `my_var` to a string. However, more complex variables might require special care. We support adding instructions for these conversions though the `hooks` parameter of `to_dataclass`.

`hooks` is intended to be a dictionary which maps a field's data type to a function which should handle the conversion. As an example, consider a data type such as `datetime`. Imagine we're working with an API which returns timestamps as ISO strings, and we'd like to convert them to `datetime` so we can perform logic with them. We can accomplish this by leveraging `hooks`:
```
from dataclasses import dataclass
from datacasting import to_dataclass

from datetime import datetime
import some_api

@dataclass
class User:
    username: str
    bio: str
    date_joined: datetime

""" Returns a User object
"""
def find_user(id: str) -> User:
    # Get the user from the API. API calls often return results as a dictionary.
    user_dict = some_api.get_user(id)

    # We create a hook that instructs to_dataclass to use 'fromisoformat' to convert any values to datetime.
    my_hooks = {
        datetime: datetime.fromisoformat
    }

    # Finally, we perform the conversion, and return a User object.
    user = to_dataclass(User, user_dict, hooks=my_hooks)
    return user
```

## How it Works
`datacasting` uses the type hints of your dataclass to determine how to cast incoming data. It matches those data types to the fields of your input dictionary, and attempts to convert the field values.

## Pitfalls and Limitations
### Unions
The `typing.Union` data type can sometimes lead to confusing results. When you specify a `Union`, `to_dataclass` will use each data type specified **in the order they are written**. This means that if you write `Union[str, float]`, then `to_dataclass` will attempt to cast your value to a `str` before an `float`, which may not be what you intent. We remedy this partially by checking the type of the input value; for example, if the value is already a `float`, then we won't try to convert it. However, if the value were an `int`, it would be cast to `str` rather than `float`, which may confuse you later in your code. For this purpose, we recommend you order the types inside a `Union` from most-to-least restrictive.

### List[...], Tuple[...], Dict[...], etc.
Often when specifying dataclasses, you can use `List[str]` to denote a list in which all the entries are strings. Various type checkers and linters take this into account, but `datacasting` doesn't perform any casting on the items of container items. What this means is that if your dataclass specifies `Tuple[int, int]` but the input dictionary has `('1', '5')`, `to_dataclass` will not attempt to convert any of the tuple entries to ints.

### Non-typing syntax
Newer versions on Python support simpler type-hint syntax:
```
class MyClass:
    list_of_strings: list[str]
    int_or_float: int | float
    ...
```
Currently, `datacasting` isn't configured to correctly understand these type hints, but that is a plan for future release.