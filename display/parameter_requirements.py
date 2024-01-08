"""
Comparison Method Decorator

This module defines a decorator for marking functions as comparison methods.
It includes exceptions for handling non-decorated functions and
functions with incorrect parameters.

Classes:
- NotDecoratedError: Exception for attempting to use a non-decorated function for
                     comparisons.
- ParameterError: Exception for a function having incorrect parameters.

Functions:
- comparison_method: Decorator for marking functions as comparison methods.
    Usage:
    @comparison_method
    def my_comparison_function(system1_election, system2_election):
        ...
- check_comparison_method: checks if a function has been decorated.
"""

import functools
import inspect


class NotDecoratedError(BaseException):
    """
    Exception for attempting to use a non-decorated function for comparisons.
    """


class ParameterError(BaseException):
    """
    Exception for a function having incorrect parameters.
    """


def comparison_method(func: callable) -> callable:
    """
    Decorator for marking functions as comparison methods.

    :param func: The function to be decorated.
    :type func: callable
    :return: The decorated function.
    :rtype: callable
    :raises ParameterError: If the decorated function does not have the
            expected parameters.
    """
    expected_parameters = ["system1_election", "system2_election"]

    signature = inspect.signature(func)
    function_parameters = [param.name for param in signature.parameters.values()]

    if expected_parameters != function_parameters:
        raise ParameterError(
            f"""Function {func.__name__} must only have the parameters
            " system1_election, system2_election"
            """)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    setattr(wrapper, 'comparison_method', True)

    return wrapper


def check_comparison_method(display_method):
    if not getattr(display_method, 'comparison_method', False):
        raise NotDecoratedError(
            f"Function {display_method.__name__} "
            f"must be decorated with @comparison_method")
