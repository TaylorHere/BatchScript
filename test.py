from BatchScript.master import Master
from BatchScript.worker import Worker
import BatchScript.helper
import BatchScript.config
import time
def timer(id):
    for i in range(10 ** 6):
        _ = 1 + 1
    return id, time.time()

master = Master(func=timer, worker=Worker, result_callback=print)
master.start()

for i in range(5000):
    master.jobs().put(i)

from queue import Empty

results = []
while True:
    results.append(master.results().get())  #this will return one results queue by round robin
    if len(results) == 5000:
        break

print("\033[32m Run with BatchScript \033[0m")
print(len(results))
results = sorted(results, key=lambda x: x[1])
_, start = results[0]
_, end = results[-1]
print(end-start)

master.stop()

results = []
for i in range(5000):
    results.append(timer(i))

print("\033[31m Run in a loop \033[0m")
print(len(results))
results = sorted(results, key=lambda x: x[1])
_, start = results[0]
_, end = results[-1]
print(end-start)

