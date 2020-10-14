from queue import Queue as ThreadQueue
from queue import Empty
from multiprocessing import Queue as ProcessQueue
from concurrent.futures import ThreadPoolExecutor, as_completed

import BatchScript.config
import time
import signal

class Worker(object):

    func = None
    jobs = None
    executor = None
    results = None
    config = BatchScript.config

    p = None

    def __init__(self, func, jobs: ThreadQueue, results: ProcessQueue, config=None):
        self.func = func
        self.jobs = jobs
        self.results = results
        if config:
            self.config = config
        self.executor = ThreadPoolExecutor(self.config.MaxThreadPoolSize)

        def shutdown(signalnum, frame):
            exit(0)
        for sig in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM]:
            signal.signal(sig, shutdown)

    def start(self):
        while True:
            job_datas = []
            for _ in range(self.config.WorkerGetBatchSize):
                try:
                    job_datas.append(self.jobs.get(timeout=self.config.ThreadQueueWaitTimeout))
                except Empty:
                    break
            works = []
            batch_submit = time.time()
            for job_data in job_datas:
                works.append(self.executor.submit(self.func, job_data))
            work_results = []
            for work in as_completed(works):
                if not self.config.ResultsBatch:
                    self.results.put(work.result())
                else:
                    work_results.append(work.result())
            if self.config.ResultsBatch and work_results:
                self.results.put(work_results)
            batch_completed = time.time()
            if job_datas:
                job_data_count = len(job_datas)
                timedelta = batch_completed - batch_submit
                speed = job_data_count / timedelta
                print("run \033[32m{}\033[0m in batch completed in \033[32m{:.2f}\033[0m seconds with \033[32m{}\033[0m job_datas speed \033[32m{:.2f}\033[0m/s".format(self.func.__name__, timedelta, job_data_count, speed))
