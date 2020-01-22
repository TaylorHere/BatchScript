from master import Master
from worker import Worker

from queue import Queue as ThreadQueue
from multiprocessing import Queue as ProcessQueue

from multiprocessing import Process
import helper 

master = Master(func=helper.sleep, worker=Worker, result_callback=print)
master.start()
for id, (jobs, _) in master.jobs_results.items():
    for i in range(100):
        jobs.put(0.01)

master.handle_results()
