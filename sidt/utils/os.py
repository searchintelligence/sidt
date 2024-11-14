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
        target_dir = target_dir.replace('/', '\\')
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


def get_root_path(current_directory=".", max_depth=3, look_for=[".git", "requirements.txt"]):
    """
    Returns the root directory path of the current project by traversing up from the current file directory
    until it finds a directory containing both a .git folder and a requirements.txt file.

    Returns:
        str: The path to the root directory of the project, or None if no such directory is found.
    """

    for _ in range(max_depth):
        if all(os.path.exists(os.path.join(current_directory, item)) for item in look_for):
            return current_directory
        current_directory = os.path.dirname(current_directory)


def validate_path(path, expected_extension=None, is_file=True, read_access=False, write_access=False, allow_empty=False) -> bool:
    """
    Validates the given path based on the specified criteria.
    Raises exceptions if the path is invalid.
    
    Args:
        path (str): Path of the file or directory to be validated.
        expected_extension (str, optional): Expected file extension for files. Defaults to None.
        is_file (bool, optional): Set to True to validate as a file, False to validate as a directory. Defaults to True.
        read_access (bool, optional): Check read access. Defaults to False.
        write_access (bool, optional): Check write access. Defaults to False.
        allow_empty (bool, optional): Allow empty files or folders. Defaults to False.
        
    Returns:
        bool: True if the path is valid.
    """
    if not isinstance(path, str):
        raise TypeError(f"Path must be a string: {path}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")

    # Check if it's a file or directory
    if is_file:
        if not os.path.isfile(path):
            raise ValueError(f"Expected a file, but found a directory: {path}")
        if expected_extension and not os.path.splitext(path)[1].lower() == expected_extension.lower():
            raise ValueError(f"Invalid file type: {path}")
        if not allow_empty and os.path.getsize(path) == 0:
            raise ValueError(f"Empty file: {path}")
    else:
        if not os.path.isdir(path):
            raise ValueError(f"Expected a directory, but found a file: {path}")
        if not allow_empty and not os.listdir(path):
            raise ValueError(f"Empty directory: {path}")

    # Check read and write access
    if read_access and not os.access(path, os.R_OK):
        raise PermissionError(f"Read permission denied: {path}")
    if write_access and not os.access(path, os.W_OK):
        raise PermissionError(f"Write permission denied: {path}")

    return True
    

def get_available_funcs(module, exclude_private=True, exclude_module=True):
    """
    Returns a list of available functions in the specified module.
    
    Args:
        module (module): The module to inspect.
        exclude_private (bool, optional): Exclude private functions (starting with '_'). Defaults to True.
        exclude_module (bool, optional): Exclude functions from imported modules. Defaults to True.
        
    Returns:
        list: List of available function names.
    """
    
    available_functions = [
        name for name, obj in module.__dict__.items() 
        if callable(obj) 
        and (not exclude_private or not name.startswith("_"))
        and (not exclude_module or obj.__module__ == module.__name__)
    ]
    return available_functions
