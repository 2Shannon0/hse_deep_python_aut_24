from functools import wraps
from typing import Callable, List, Dict, Type, Optional, Any


def to_log(func_name: str, call_data: Dict[str, Any]):

    attempt = call_data.get("attempt")
    args = call_data.get("args", ())
    kwargs = call_data.get("kwargs", {})
    result = call_data.get("result", None)
    exception = call_data.get("exception", None)
    if exception:
        if args and kwargs:
            print(f'run "{func_name}" with positional args = {args}, '
                  f'keyword kwargs = {kwargs}, attempt = {attempt}, '
                  f'exception = {type(exception).__name__}')
        elif args:
            print(f'run "{func_name}" with positional args = {args}, '
                  f'attempt = {attempt}, '
                  f'exception = {type(exception).__name__}')
        else:
            print(f'run "{func_name}" with keyword kwargs = {kwargs}, '
                  f'attempt = {attempt}, '
                  f'exception = {type(exception).__name__}')
    else:
        if args and kwargs:
            print(f'run "{func_name}" with positional args = {args}, '
                  f'keyword kwargs = {kwargs}, '
                  f'attempt = {attempt}, result = {result}')
        elif args:
            print(f'run "{func_name}" with positional args = {args}, '
                  f'attempt = {attempt}, result = {result}')
        else:
            print(f'run "{func_name}" with keyword kwargs = {kwargs}, '
                  f'attempt = {attempt}, result = {result}')


def retry_deco(
        retries: int = 3,
        expected_exceptions: Optional[List[Type[BaseException]]] = None
        ) -> Callable:

    expected_exceptions = expected_exceptions or []

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                attempt += 1
                try:
                    result = func(*args, **kwargs)
                    to_log(func.__name__, {
                        "args": args,
                        "kwargs": kwargs,
                        "attempt": attempt,
                        "result": result
                    })
                    return result
                except Exception as e:  # pylint: disable=broad-except
                    if any(isinstance(e, exc) for exc in expected_exceptions):
                        to_log(func.__name__, {
                            "args": args,
                            "kwargs": kwargs,
                            "attempt": attempt,
                            "exception": e
                        })
                        return None
                    to_log(func.__name__, {
                        "args": args,
                        "kwargs": kwargs,
                        "attempt": attempt,
                        "exception": e
                    })
            return None
        return wrapper
    return decorator


@retry_deco(3)
def add(a, b):
    return a + b


@retry_deco(3)
def check_str(value=None):
    if value is None:
        raise ValueError()
    return isinstance(value, str)


@retry_deco(2, [ValueError])
def check_int(value=None):
    if value is None:
        raise ValueError()
    return isinstance(value, int)
