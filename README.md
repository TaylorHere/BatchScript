BatchScript

使用多进程+线程池运行你的方法

~~~python
from master import Master
from worker import Worker

from queue import Queue as ThreadQueue
from multiprocessing import Queue as ProcessQueue

from multiprocessing import Process
import helper 

#启动master
master = Master(func=helper.sleep, worker=Worker, result_callback=print)
master.start()
for id, (jobs, _) in master.jobs_results.items():
    for i in range(100):
        jobs.put(0.01)

#处理结果
master.handle_results()
#或者
while True:
    try:
        for id, (_, results) in self.jobs_results.items():
            result = results.get()
            self.result_callback(result)
    except Empty:
        continue
~~~

采用 多进程启动Worker, worker维护线程池运行函数的方案
master内建和worker关联的多个任务队列和对应的多个结果队列
worker按batch从任务队列中获取数据并使用线程池提交运行
批量结束后将任务结果put到结果队列

你可以在config.py文件中调整

MaxWorkerSize = os.cpu_count() - 1 #worker数量
MaxThreadPoolSize = 1024 #每个worker的线程池大小
threadQueueWaitTimeout = 0.01 #worker在job队列上获取数据的超时, 超时后会立即开始批量线程提交
WorkerGetBatchSize = 100 #额定批大小, 如果worker获取数据时不超时, 那么在获取都这个数量后便开始批量线程提交
JobsResultsQueueNum = MaxWorkerSize #jobs 和 results 队列对的数量, 该数量如果小于worker数量, 则最后一对会被未分配的worker共用, 共用队列可能会导致锁操作增加
