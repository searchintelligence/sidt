import time
import random
from functools import wraps

from tqdm import tqdm

from ..utils.io import CLIF


def retry(n_attempts=3, wait=0, exponential_backoff=False, randomise_wait=True, catch_types=Exception, show_tracker=True, require_input=False):
    """
    A decorator that retries a function execution a specified number of times with an optional wait between attempts.
    Supports exponential backoff and catching multiple exception types.

    Parameters:
    n_attempts (int): Maximum number of attempts to execute the function.
    wait (int or float): Time to wait between retries in seconds, defaulting to 0 for instant retries.
    exponential_backoff (bool): If True, doubles the wait time after each attempt.
    randomise_wait (bool): If true, wait time will be multiplied by a random factor between 0.8 and 1.2.
    catch_types (Exception or tuple/list of Exceptions): The exception(s) to catch and retry on. Can be a single exception type or a tuple/list of exception types.
    show_tracker (bool): If true, a tqdm progress bar will show the number of remaining attempts.
    
    Usage:
    @retry(n_attempts=3, wait=2, exponential_backoff=True, catch_types=(ValueError, KeyError))
    def risky_function():
        "Code that might fail"
    """

    def calculate_wait_time(attempt, base_wait, use_exponential_backoff, use_random):
        """Calculate the wait time based on the current attempt number."""
        sleep_time = base_wait * (2 ** (attempt - 1)) if use_exponential_backoff else base_wait
        return random.uniform(sleep_time * 0.8, sleep_time * 1.2) if use_random else sleep_time


    def get_desc(attempt, n_attempts, exception, sleep_time, require_input):
        """Determine the current status and error information."""
        if attempt >= n_attempts:
            status = f"(No attempts remaining)"
        else:
            status = f"(Attempt {attempt + 1} of {n_attempts})"
        desc = ( CLIF.fmt(f"{status} | Error: {exception}", CLIF.Color.RED, CLIF.Format.BOLD) +
                 CLIF.fmt(f" | Retrying in {round(sleep_time, 2)}s", CLIF.Color.YELLOW, CLIF.Format.BOLD) )
        if require_input:
            desc += CLIF.fmt(" | Press any key to try again", CLIF.Color.YELLOW, CLIF.Format.BOLD)
        return desc


    def normalise_catch_types(catch_types):
        """Ensure the catch_types is in tuple form."""
        if not isinstance(catch_types, tuple):
            return (catch_types,) if isinstance(catch_types, type) else tuple(catch_types)
        return catch_types


    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            norm_catch_types = normalise_catch_types(catch_types)
            tracker = tqdm(
                total=n_attempts, 
                desc=CLIF.fmt(f"(Attempt 1 of {n_attempts})", CLIF.Color.GREEN, CLIF.Format.BOLD), 
                leave=False, 
                dynamic_ncols=True) if show_tracker else None
            attempts = 0

            while attempts < n_attempts:
                try:
                    result = func(*args, **kwargs)
                    if show_tracker:
                        tracker.close()
                    return result
                except norm_catch_types as e:
                    attempts += 1
                    sleep_time = calculate_wait_time(attempts, wait, exponential_backoff, randomise_wait)
                    desc = get_desc(attempts, n_attempts, e, sleep_time, require_input)                        
                    if show_tracker:
                        tracker.set_description(desc)
                    if attempts == n_attempts:
                        raise
                    if require_input:
                        input("\n\n")
                    time.sleep(sleep_time)
            if show_tracker:
                tracker.close()

        return wrapper
    return decorator


def time_function(func):
    """
    Decorator that measures the execution time of a function and returns the function's
    result along with the time taken to execute it.

    Usage:
        @time_function
        def example_function(args):
            # function implementation
            return result

        result, execution_time = example_function(args)
        print(result, execution_time)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        return result, duration
    return wrapper