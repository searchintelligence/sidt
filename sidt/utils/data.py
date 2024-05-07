
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


def excel_column_converter(value):
    """
    Converts between a bijective base-26 number and its corresponding alphabetic string and vice versa.

    Args:
        value (int or str): Numeric index or alphabetic string to be converted.

    Example:
    - excel_column_converter(1) -> 'A'
    - excel_column_converter('A') -> 1
    - excel_column_converter(28) -> 'AB'
    - excel_column_converter('AB') -> 28
    """

    # Convert integer to string
    if isinstance(value, int):
        if value < 1:
            raise ValueError("Index must be at least 1.")
        name = []
        while value > 0:
            value, remainder = divmod(value - 1, 26)
            name.append(chr(65 + remainder))
        return ''.join(reversed(name))
    
    # Convert string to integer
    elif isinstance(value, str):
        number = 0
        for char in value.upper():
            if not char.isalpha() or ord(char) < ord('A') or ord(char) > ord('Z'):
                raise ValueError("String must consist only of uppercase letters from A to Z.")
            number = number * 26 + (ord(char) - ord('A') + 1)
        return number
    
    else:
        raise TypeError("Input must be an integer or a string.")