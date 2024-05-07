
def nested_lookup(nested_item, lookup_keys):
    """
    Safely navigates through a nested dictionary/list structure and retrieves 
    a value using a specified list of keys/indices.

    Parameters:
        nested_item (dict or list): The nested dictionary or list.
        lookup_keys (list): A list of keys or indices specifying the path to the desired value.

    Returns:
        The value found at the path, or None if the path is invalid or an error occurs.

    Example:
        data = response.json()  # Assume response.json() returns a list or dict
        result = Tools.nested_lookup(data, [0, "key", 5, "title", "value"])
    """

    current = nested_item
    try:
        for key in lookup_keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and isinstance(key, int) and key < len(current):
                current = current[key]
            else:
                return None
    except (TypeError, IndexError, KeyError):
        return None

    return current


def flatten_structure(structure):
    """
    Recursively flattens a nested list of lists and dictionaries to a single-level list.

    Example:
    flatten([1, [2, [3, 4]], 5, {'a': 6}])
        [1, 2, 3, 4, 5, {'a': 6}]
    """

    result = []
    for item in structure:
        if isinstance(item, (list, tuple, set)):
            # Recursively flatten lists, tuples, and sets
            result.extend(flatten_structure(item))
        else:
            # Append all other types directly
            result.append(item)
    return result

