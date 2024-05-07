import csv
import os
import sys
import inspect
import subprocess
from dataclasses import asdict, fields
from enum import Enum

import pandas as pd


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


def dump(data, filename):
    # data must be a dataclass object or list of the same dataclass objects

    origin = os.path.splitext(os.path.basename(inspect.stack()[1].filename))[0]
    os.makedirs(os.path.join("out", origin), exist_ok=True)
    path = os.path.join("out", origin, filename + ".csv")

    field_names = [f.name for f in fields(data[0])]

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for item in data:
            writer.writerow(asdict(item))


def get_current_path():
    """
    Returns the absolute directory path of the python file from which this function is called.
    """

    caller_frame = inspect.stack()[1]
    caller_path = caller_frame.filename
    caller_directory = os.path.dirname(os.path.abspath(caller_path))
    return caller_directory


def xlsx_to_dfs(file_path):
    """
    Reads an Excel file and returns a dictionary of DataFrames, one for each sheet.

    Parameters:
    file_path (str): The path to the Excel (.xlsx) file.

    Returns:
    dict: A dictionary where keys are sheet names and values are DataFrames corresponding to each sheet.
    """

    return pd.read_excel(pd.ExcelFile(file_path), sheet_name=None, index_col=None)


def dfs_to_xlsx(dfs, file_path):
    """
    Writes a dictionary of DataFrames to an Excel file, with each DataFrame as a separate sheet.

    Parameters:
    dfs (dict): A dictionary where keys are sheet names and values are DataFrames.
    file_path (str): The path where the Excel (.xlsx) file will be saved.
    """

    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name)


def open_dir(target_dir, return_pid=False):
    """
    Opens a directory or file in the system's default file explorer or associated application.
    Supports Windows, macOS, and Linux operating systems.

    Args:
        target_dir (str): The directory path to open.
        return_pid (bool): If True, returns the process ID (int) of the file explorer.
    """

    process = None
    if sys.platform == "win32":
        process = subprocess.Popen(["explorer", target_dir])
    elif sys.platform == "darwin":
        process = subprocess.Popen(["open", target_dir])
    else:
        process = subprocess.Popen(["xdg-open", target_dir])
    
    if return_pid:
        return process.pid

