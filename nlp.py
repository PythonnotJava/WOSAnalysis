from collections.abc import Iterable

def is_iterable(obj):
    return isinstance(obj, Iterable)
print(is_iterable({}.keys()))