from master import Master
from worker import Worker
import helper 

master = Master(func=helper.sleep, worker=Worker, result_callback=print)
master.start()
for i in range(1000):
    master.job_put(0.01)

while True:
    print(master.result_get())
