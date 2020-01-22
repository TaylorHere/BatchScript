from master import Master
from worker import Worker
import helper 

master = Master(func=helper.sleep, worker=Worker, result_callback=print)
master.start()
for id, (jobs, _) in master.jobs_results.items():
    for i in range(100):
        jobs.put(0.01)

master.handle_results()
