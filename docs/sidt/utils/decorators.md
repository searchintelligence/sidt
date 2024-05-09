# Decorators

[Sidt Index](../../README.md#sidt-index) / [Sidt](../index.md#sidt) / [Utils](./index.md#utils) / Decorators

> Auto-generated documentation for [sidt.utils.decorators](../../../sidt/utils/decorators.py) module.

- [Decorators](#decorators)
  - [retry](#retry)
  - [time_function](#time_function)

## retry

[Show source in decorators.py:12](../../../sidt/utils/decorators.py#L12)

A decorator that retries a function execution a specified number of times with an optional wait between attempts.
Supports exponential backoff and catching multiple exception types.

#### Arguments

- `n_attempts` *int* - Maximum number of attempts to execute the function.
wait (int or float): Time to wait between retries in seconds, defaulting to 0 for instant retries.
- `exponential_backoff` *bool* - If True, doubles the wait time after each attempt.
- `randomise_wait` *bool* - If true, wait time will be multiplied by a random factor between 0.8 and 1.2.
catch_types (Exception or tuple/list of Exceptions): The exception(s) to catch and retry on. Can be a single exception type or a tuple/list of exception types.
- `show_tracker` *bool* - If true, a tqdm progress bar will show the number of remaining attempts.

Usage:
@retry(n_attempts=3, wait=2, exponential_backoff=True, catch_types=(ValueError, KeyError))
def risky_function():
    "Code that might fail"

#### Signature

```python
def retry(
    n_attempts=3,
    wait=0,
    exponential_backoff=False,
    randomise_wait=True,
    catch_types=Exception,
    show_tracker=True,
    require_input=False,
): ...
```



## time_function

[Show source in decorators.py:92](../../../sidt/utils/decorators.py#L92)

Decorator that measures the execution time of a function and returns the function's
result along with the time taken to execute it.

Usage:
    @time_function
    def example_function(args):
        # function implementation
        return result

result, execution_time = example_function(args)
print(result, execution_time)

#### Signature

```python
def time_function(func): ...
```