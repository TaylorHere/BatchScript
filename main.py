from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

import time


def timeit(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        a = time.time()
        func(*args, **kwargs)
        b = time.time()
        print(func.__name__, b - a)
    return wrapper


def sleep():
    for i in range(10**6):
        _ = 1 + 1
    time.sleep(0.03)

def threadPool(f, t_works=1024, t_workers=1024, *args, **kwargs):
    works = []
    with ThreadPoolExecutor(t_workers) as executor:
        for i in range(t_works):
            works.append(executor.submit(f, *args, **kwargs))
    for work in as_completed(works):
        work.result()

def processPool(f, p_workers=3, p_works=3, t_works=1024, t_workers=1024, *args, **kwargs,):
    works = []
    with ProcessPoolExecutor(p_workers) as executor:
        for i in range(p_works):
            works.append(executor.submit(threadPool, f, t_workers=t_workers, t_works=t_works, *args, **kwargs))
    for work in as_completed(works):
        work.result()

import os

@timeit
def submit(f, concurrency, *args, **kwargs):
    p_workers = os.cpu_count() * 2 - 1
    p_works = p_workers
    t_workers = int(concurrency / p_workers)
    t_works = t_workers
    print('concurrency', concurrency, 'p', p_workers, 't', t_workers)
    processPool(f, p_workers=p_workers, t_workers=t_workers, p_works=p_works, t_works=t_works, *args, **kwargs)

submit(sleep, 50)

