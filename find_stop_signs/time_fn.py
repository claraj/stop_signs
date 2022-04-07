import functools 
import time

def timer(func):
    @functools.wraps(func)
    def timeit(*args, **kwargs):
        start = time.perf_counter()
        print(f'Starting {func.__name__}')
        func(*args, **kwargs)
        end = time.perf_counter()
        run_time = end - start 
        print(f'{func.__name__} completed, taking {run_time} seconds')
    return timeit


