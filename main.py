from master import Master
from worker import Worker
from consumer import Consumer


master = Master(func=helper.sleep, worker=Worker, result_callback=print)
master.start()

queue_id = 0

def get_queue():
    queue = master.jobQueues[queue_id]
    if queue_id + 1 > len(master.jobQueues):
        queue_id = 0
    else:
        queue_id += 1

def put_in_queue(msg):
    queue = get_queue()
    queue.put(msg)

Consumer(callback=put_in_queue).start()