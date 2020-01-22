import config
from queue import Queue as ThreadQueue
from queue import Empty
from multiprocessing import Queue as ProcessQueue
from concurrent.futures import ThreadPoolExecutor, as_completed

class Worker(object):

    func = None
    jobs = None
    executor = ThreadPoolExecutor(config.MaxThreadPoolSize)
    results = None

    def __init__(self, func, jobs: ThreadQueue, results: ProcessQueue):
        self.func = func
        self.jobs = jobs
        self.results = results

    def start(self):
        print('worker start')
        while True:
            items = []
            for i in range(config.WorkerGetBatchSize):
                try:
                    items.append(self.jobs.get(timeout=config.threadQueueWaitTimeout))
                except Empty:
                    break
            works = []
            for item in items:
                works.append(self.executor.submit(self.func, item))
            for work in as_completed(works):
                self.results.put(work.result())

