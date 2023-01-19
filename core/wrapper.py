import cProfile
import pstats
import threading

from functools import wraps


def async_func(func):
    """
    Thread Decorator

    Run the function in asynchronous
    """
    @wraps(func)
    def _wrapper_view(*args, **kwargs):
        thread = threading.Thread(
            target=func,
            name='Thread-async',
            args=args,
            kwargs=kwargs
        )
        thread.start()

    return _wrapper_view


def profile(func=None, repeat=None):
    """
    Profile with cProfiler

    Run function in profile mode
    usage: wrap a function to profile with @profile(repeat=N)
    """
    def inner(func):
        @wraps(func)
        def _wrapper_view(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()
            print('\n# cProfile %s x %d' % (func.__name__, repeat))

            for i in range(repeat):
                func(*args)

            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('tottime')
            stats.print_stats()

        return _wrapper_view
    return inner
