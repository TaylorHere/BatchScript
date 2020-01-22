from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import Queue as ProcessQueue
from multiprocessing import Process
from queue import Queue as ThreadQueue
from queue import Empty
from concurrent.futures import ProcessPoolExecutor, as_completed
import config



class Master(object):

    worker = None
    resultsQueueClass = ProcessQueue
    jobsQueueClass = ProcessQueue
    workers = []
    jobs_results = {}
    result_callback = None
    func = None

    def __init__(self, func, result_callback, worker, jobsQueueClass=None, resultsQueueClass=None):
        self.worker = worker
        self.result_callback = result_callback
        self.func = func
        if jobsQueueClass:
            self.jobsQueueClass = jobsQueueClass
        if resultsQueueClass:
            self.resultsQueueClass = resultsQueueClass
        self.jobs_results = {}
        for i in range(config.JobsResultsQueueNum):
            jobs = self.jobsQueueClass()
            results = self.resultsQueueClass()
            self.jobs_results[i] = (jobs, results)

    def start_worker(self,):
        for i in range(config.MaxWorkerSize):
            if i > len(self.jobs_results):
                i = len(self.jobs_results) - 1
            jobs, results = self.jobs_results[i]
            worker = self.worker(func=self.func, jobs=jobs, results=results)
            p = Process(target=worker.start)
            p.start()
            self.workers.append(p)
        print('start {} workers'.format(len(self.workers)))

    class fair_choice():
        queue_id = 0
        def get(self, jobs_results):
            if self.queue_id + 1 >= len(jobs_results):
                self.queue_id = 0
            else:
                self.queue_id += 1
            return self.queue_id
    fair_choice = fair_choice()

    def job_put(self, job, func=fair_choice.get):
        jobs, _ = self.jobs_results[func(self.jobs_results)]
        jobs.put(job)

    def result_get(self, func=fair_choice.get):
        _, results = self.jobs_results[func(self.jobs_results)]
        return results.get()

    def start(self,):
        p = Process(target=self.start_worker)
        p.start()
        return p

    def handle_results(self,):
        while True:
            for id, (_, results) in self.jobs_results.items():
                try:
                    result = results.get()
                    self.result_callback(result)
                except Empty:
                    continue
