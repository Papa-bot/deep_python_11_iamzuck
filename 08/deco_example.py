import cProfile
from io import StringIO
import pstats
import functools


def profile_deco(target_func):
    profiler = cProfile.Profile()

    @functools.wraps(target_func)
    def wrapped_func(*args, **kwargs):
        profiler.enable()
        result = target_func(*args, **kwargs)
        profiler.disable()
        return result

    def display_stats():
        output = StringIO()
        stats = pstats.Stats(profiler, stream=output)
        stats.strip_dirs()
        stats.sort_stats("cumulative")
        stats.print_stats()
        print(output.getvalue())

    wrapped_func.display_stats = display_stats
    return wrapped_func


if __name__ == "__main__":

    @profile_deco
    def add_values(x, y):
        return x + y

    @profile_deco
    def subtract_values(a, b):
        return a - b

    for _ in range(1_000_000):
        add_values(1, 2)
        subtract_values(4, 5)

    print("Add function stats:")
    add_values.display_stats()

    print("\nSubtract function stats:")
    subtract_values.display_stats()
