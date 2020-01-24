import time


def sleep(timeout):
    for i in range(10 ** 6):
        _ = 1 + 1
    # print('wake up')
    return 'wake up'
    # time.sleep(timeout)
    # return timeout

def timer(id):
    for i in range(10 ** 6):
        _ = 1 + 1
    return id, time.time()

def timeit(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        a = time.time()
        func(*args, **kwargs)
        b = time.time()
        print(func.__name__, b - a)
    return wrapper
