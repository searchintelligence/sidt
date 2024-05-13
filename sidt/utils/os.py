import os
import sys
import inspect
import subprocess


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


def get_current_path():
    """
    Returns the absolute directory path of the python file from which this function is called.
    """

    caller_frame = inspect.stack()[1]
    caller_path = caller_frame.filename
    caller_directory = os.path.dirname(os.path.abspath(caller_path))
    return caller_directory
