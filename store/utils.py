from typing import Any, Iterable



def flattened(iterable: Iterable) -> list[Any]:
    """
    Get a flattened copy of a given iterable.
    :param iterable: The iterable to get a flattened copy of.
    :return: The 1D list consisting of the iterable's elements.
    """
    flat: list[Any] = []
    for element in iterable:
        if (isinstance(element, Iterable)) and (not isinstance(element, (str, bytes))):
            flat.extend(flattened(element))
        else:
            flat.append(element)
    return flat
