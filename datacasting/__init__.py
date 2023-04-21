from dataclasses import is_dataclass, fields

from ._util import get_types

""" Tries to create an instance of the dataclass 'class_' using the entries in the dictionary
'dict_'. Will recursively perform on members of the dataclass which are also dataclasses. The
optional parameter 'hooks' is a mapping of functions to use for casting specific data types. It is
useful for cases like datetime, where you might already have a function for casting strings to
datetimes.
"""
def to_dataclass(class_, dict_, hooks=dict()):
    # Input Validation
    if not is_dataclass(class_):
        raise TypeError(f"'class_' must be a dataclass, but instead is {type(class_).__name__}.")
    if not isinstance(dict_, dict):
        raise TypeError(f"'dict_' must be a dictionary, but instead is {type(dict_).__name__}.")
    if not isinstance(hooks, dict):
        raise TypeError(f"'hooks' must be a dictionary, but instead is {type(hooks).__name__}.")
    if hooks:
        for key, val in hooks.items():
            if not isinstance(key, type):
                raise TypeError(f"All keys in 'hooks' must be types; got {type(key).__name__}.")
            if not callable(val):
                raise TypeError(f"Invalid value in 'hooks'; {type(val).__name__} is not callable.")

    # Store a record of dataclass fields to their type:
    types = get_types(class_)

    # Start casting
    kwargs = dict()
    for key, val in dict_.items():
        kwargs[key] = cast(val, types[key], hooks)
    
    # Pass casted values to dataclass constructor
    return class_(**kwargs)


""" Attempts to cast a value to the provided type.
"""
def cast(val, types, hooks=dict()):
    # We want to support using a list as type_ so we can iterate through the possibilities; rather
    # than dulicate the logic, it's easiest to convert single values to lists.
    try:
        [x for x in types]
    except TypeError:
        types = [types]
    
    # We want to check if the value is already one of these types, and ignore it if so.
    # We do this so that Union[str, int] won't convert 10 to "10".
    if type(val) in types:
        return val

    # Iterate through types and attempt to cast them
    for type_ in types:
        try:
            if type_ in hooks:
                return hooks[type_](val)
            if is_dataclass(type_):
                return to_dataclass(type_, val, hooks)
            return type_(val)
        except:
            pass # Ignore failures
    # If we make it here, then we couldn't successfully cast to any of the types.
    raise ValueError(f"Unable to cast '{val}' to any of: {', '.join([x.__name__ for x in types])}")