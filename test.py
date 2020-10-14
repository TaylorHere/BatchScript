from BatchScript.master import Master
from BatchScript.worker import Worker
import BatchScript.helper
import BatchScript.config
import time

#this is my function need to run in batch mode
def timer(id):
    for i in range(10 ** 6):
        _ = 1 + 1
    return id, time.time()

BatchScript.config.WorkerGetBatchSize = BatchScript.config.MaxThreadPoolSize * 10

#start a master
master = Master(func=timer, worker=Worker, result_callback=print, config=BatchScript.config)
master.start()


Job_Conut = BatchScript.config.MaxWorkerSize * 1024

#create a lot of datas
for i in range(Job_Conut):
    master.jobs().put(i)


results = []
#wait all datas done
while True:
    results.append(master.results().get())  #this will return one results queue by round robin
    if len(results) == Job_Conut:
        break

print("\033[32m Run with BatchScript \033[0m")
print(len(results))
results = sorted(results, key=lambda x: x[1])
_, start = results[0]
_, end = results[-1]
print(end-start)

#stop the master and the workers will terminated as well
master.stop()

results = []
for i in range(Job_Conut):
    results.append(timer(i))

print("\033[31m Run in a loop \033[0m")
print(len(results))
results = sorted(results, key=lambda x: x[1])
_, start = results[0]
_, end = results[-1]
print(end-start)

