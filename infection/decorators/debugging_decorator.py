""" This module defines the debugging_decorator decorator.
"""
import functools
import logging
import sys


def debugging_decorator(func):
    """ This decorator will take any function and log information about the
        function itself, its arguments, and the value it returns.
        Important: It will only log when running in debugging mode.

    Args:
        func (function): The function to decorate

    Returns:
        value (function): The function after decoration when running in
            debugging mode, otherwise the funcion is returned without
            decoration.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if sys.gettrace() is not None:
            logging.basicConfig(level=10, format="%(threadName)s:%(message)s")
            args_representation = [repr(arg) for arg in args]
            kwargs_representation = [f"{key}={value!r}"
                                     for key, value in kwargs.items()]
            arguments = ", ".join(
                args_representation + kwargs_representation)
            logging.info(
                f"Calling {func.__name__} with arguments: {arguments}")
            value = func(*args, **kwargs)
            logging.info(f"{func.__name__} returned: {value}")
            return value
        else:
            return func(*args, **kwargs)
    return wrapper
