import re


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
        result = nested_lookup(data, [0, "key", 5, "title", "value"])
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
        return "".join(reversed(name))
    
    # Convert string to integer
    elif isinstance(value, str):
        number = 0
        for char in value.upper():
            if not char.isalpha() or ord(char) < ord("A") or ord(char) > ord("Z"):
                raise ValueError("String must consist only of uppercase letters from A to Z.")
            number = number * 26 + (ord(char) - ord("A") + 1)
        return number
    
    else:
        raise TypeError("Input must be an integer or a string.")
    

def computerise_string(s, replace_spaces=None, replace_hyphens=None, no_leading_digit=False,
                       strip_all_whitespace=False, remove_problematic_chars=True, truncate_length=None,
                       to_case=None):
    """
    Formats a string based on specified parameters to make it computer-readable.

    Args:
        s (str): The input string to clean.
        replace_spaces (str, None): If specified, replaces spaces with the given string.
        replace_hyphens (str, None): If specified, replaces hyphens with the given string.
        no_leading_digit (bool): If True, adds an underscore in front of leading digits.
        strip_all_whitespace (bool): If True, removes all extra internal and external whitespace.
        remove_problematic_chars (bool, str, None): Controls removal of problematic characters.
            - True: Removes a default set of problematic characters.
            - False or None: Does not remove any problematic characters.
            - str: Removes characters specified in the provided string, e.g., "#$%&".
        truncate_length (int, None): If specified, truncates the string to this length.
        to_case (str, None): If 'lower' or 'upper', converts the string to the specified case.
    """

    if strip_all_whitespace:
        s = re.sub(r"\s+", " ", s).strip()

    if to_case == "lower":
        s = s.lower()
    elif to_case == "upper":
        s = s.upper()

    if replace_spaces:
        s = s.replace(" ", replace_spaces)

    if replace_hyphens:
        s = s.replace("-", replace_hyphens)

    if no_leading_digit and s and s[0].isdigit():
        s = "_" + s

    if isinstance(remove_problematic_chars, str):
        pattern = "[" + re.escape(remove_problematic_chars) + "]"
        s = re.sub(pattern, "", s)
    elif remove_problematic_chars is True:
        default_problematic = r'\\/*?:\[\]"<>|'
        s = re.sub("[" + re.escape(default_problematic) + "]", "", s)

    if truncate_length is not None and len(s) > truncate_length:
        s = s[:truncate_length]

    return s


def humanise_string(s, replace_underscores=True, uncapitalised_words=None, replacements=None, capitalise=True):
    """
    Converts a string to a human-readable format, with options to replace abbreviations,
    skip capitalisation of certain words, and adjust formatting.

    Args:
        s (str): The string to be humanised.
        replace_underscores (bool): If True, replaces underscores with spaces.
        uncapitalised_words (set, optional): A set of words not to capitalise if capitalise is True.
            Defaults to common English articles and prepositions.
        replacements (dict, optional): A dictionary mapping abbreviations to their desired expansions.
            Defaults to common abbreviations.
        capitalise (bool): If True, capitalises each word excluding uncapitalised words.
    """
    if not isinstance(s, str):
        raise ValueError("Input must be a string")

    # Default uncapitalised words and replacements
    if uncapitalised_words is None:
        uncapitalised_words = {
            "the", "in", "by", "and", "per", "with", "at", "from", "into", "during", "including",
            "until", "against", "among", "throughout", "despite", "towards", "upon", "of", "to",
            "for", "on", "but", "like", "over", "near", "about", "around", "as", "off", "up", "down",
            "plus", "after", "before", "under", "between"
        }
    if replacements is None:
        replacements = {
            "avg": "Avg.", "mdn": "Mdn.", "num": "No.", "id": "ID", "url": "URL", "da": "DA",
            "pr": "PR", "us": "US", "uk": "UK", "nat": "National", "api": "API", "ui": "UI",
            "ux": "UX", "qtr": "Qtr.", "yr": "Yr.", "mo": "Mo.", "hr": "Hr.", "min": "Min.",
            "sec": "Sec.", "mg": "Mg", "kg": "Kg", "dr": "DR", "eu": "EU", "un": "UN",
            "etc": "etc.", "eg": "e.g.,", "ie": "i.e.,", "vs": "vs.", "dept": "Dept.",
            "gov": "Gov.", "inc": "Inc.", "corp": "Corp."
        }

    # Process
    if replace_underscores:
        s = s.replace("_", " ")
    words = s.split()
    for i, word in enumerate(words):
        lower_word = word.lower()
        replacement = replacements.get(lower_word, None)
        if replacement:
            words[i] = replacement
        elif capitalise and (i == 0 or lower_word not in uncapitalised_words):
            words[i] = word.capitalize()

    return " ".join(words)
