from enum import Enum


class CLIF():
    """
    Command line interface formatter. Use CLIF.fmt() to format a string 
    with specified colors and formats in sequence.

    Example usage:
        print(CLIF.fmt("Hello, World!", CLIF.Color.RED, CLIF.Format.BOLD))
    """

    class Color(Enum):
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
        BRIGHT_BLACK = "\033[90m"
        BRIGHT_RED = "\033[91m"
        BRIGHT_GREEN = "\033[92m"
        BRIGHT_YELLOW = "\033[93m"
        BRIGHT_BLUE = "\033[94m"
        BRIGHT_MAGENTA = "\033[95m"
        BRIGHT_CYAN = "\033[96m"
        BRIGHT_WHITE = "\033[97m"

    class Format(Enum):
        BOLD = "\033[1m"
        DIM = "\033[2m"
        ITALIC = "\033[3m"
        UNDERLINE = "\033[4m"
        BLINK = "\033[5m"
        REVERSE = "\033[7m"
        HIDDEN = "\033[8m"
        STRIKE = "\033[9m"

    RESET = "\033[0m"

    @staticmethod
    def fmt(text, *args):
        """
        Format text with specified color and styles applied in sequence.
        
        Args:
            text (str): The text to format.
            *args: Arbitrary list of CLIF.Color and CLIF.Format to apply.

        Returns:
            str: The formatted text.
        """
        format_sequence = "".join(arg.value for arg in args)
        return f"{format_sequence}{text}{CLIF.RESET}"


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
