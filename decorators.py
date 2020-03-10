import functools
import time
from helpers import append_to_file
from django.conf import settings

def timer(function):
    """
    Decorator used to print the runtime of a function in seconds.
    To use simply place "@timer" above a function declaration.
    For nanoseconds use perf_counter_ns for start and end times.
    For seconds use perf_counter for start and end times.
    Args:
        function: the name of the function to time
    
    Returns:
        The result of the function the decorator is called on
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        function_value = function(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        log_text = f"{function.__name__} ran in {run_time} seconds\n"
        print(log_text)
        print(f"writing to file {settings.LOGFILE}")
        append_to_file(log_text, settings.LOGFILE)
        return function_value
    return wrapper