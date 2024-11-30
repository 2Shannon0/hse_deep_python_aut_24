import cProfile
import pstats
from functools import wraps


def profile_deco(func):
    profiler = cProfile.Profile()
    stats = None

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal stats
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()

        if stats is None:
            stats = pstats.Stats(profiler)
        else:
            stats.add(pstats.Stats(profiler))
        return result

    def print_stat():
        if stats is not None:
            stats.print_stats()

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)


add.print_stat()
sub.print_stat()
