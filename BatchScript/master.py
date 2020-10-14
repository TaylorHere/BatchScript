from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Queue as ProcessQueue
from multiprocessing import Process
from queue import Queue as ThreadQueue
from queue import Empty
from concurrent.futures import ProcessPoolExecutor, as_completed
import signal

import BatchScript.config

from BatchScript.worker import Worker



class Master(object):

    worker = None
    resultsQueueClass = ProcessQueue
    jobsQueueClass = ProcessQueue
    workers = []
    jobs_results = {}
    result_callback = None
    func = None
    config = BatchScript.config

    def __init__(self, func, connection=None, result_callback=None, worker=Worker, jobsQueueClass=None, resultsQueueClass=None, config=None, *args, **kwargs):
        self.worker = worker
        self.result_callback = result_callback
        self.func = func
        if config:
            self.config = config
        if worker:
            self.worker = worker
        if jobsQueueClass:
            self.jobsQueueClass = jobsQueueClass
        if resultsQueueClass:
            self.resultsQueueClass = resultsQueueClass
        self.jobs_results = {}
        for i in range(self.config.JobsResultsQueueNum):
            if not connection:
                jobs = self.jobsQueueClass()
                results = self.resultsQueueClass()
                self.jobs_results[i] = (jobs, results)
            else:
                results = self.resultsQueueClass()
                self.jobs_results[i] = (connection.results(*args, **kwargs), results)

    def start_worker(self,):
        for i in range(self.config.MaxWorkerSize):
            if i > len(self.jobs_results):
                i = len(self.jobs_results) - 1
            jobs, results = self.jobs_results[i]
            worker = self.worker(func=self.func, jobs=jobs, results=results, config=self.config)
            p = Process(target=worker.start)
            p.start()
            worker.p = p
            self.workers.append(worker)
        print('start {} workers'.format(len(self.workers)))

    class RoundRobin():
        queue_id = 0
        def get(self, jobs_results):
            if self.queue_id + 1 >= len(jobs_results):
                self.queue_id = 0
            else:
                self.queue_id += 1
            return self.queue_id

    jobs_round_robin = RoundRobin()
    def jobs(self, func=jobs_round_robin.get):
        _jobs, _ = self.jobs_results[func(self.jobs_results)]
        return _jobs

    results_round_robin = RoundRobin()
    def results(self, func=results_round_robin.get):
        _, _results = self.jobs_results[func(self.jobs_results)]
        return _results

    def start(self,):
        self.start_worker()

    def handle_results(self, *args, **kwargs):
        while True:
            try:
                result = self.results.get(*args, **kwargs)
                self.result_callback(result)
            except Empty:
                continue
    
    def stop(self,):
        for worker in self.workers:
            worker.p.terminate()
            worker.p.join()
            print(f"worker {worker.p.pid}, closed")