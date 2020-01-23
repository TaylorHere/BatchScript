from master import Master
from worker import Worker
from consumer import Consumer


master = Master(func=helper.sleep, worker=Worker, result_callback=print)
master.start()

Consumer(callback=master.jobs().put).start()