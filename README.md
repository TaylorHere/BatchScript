BatchScript

使用多进程+线程池+队列运行你的方法

~~~shell
$> pip3 install BatchScript
# or
$> git clone https://github.com/TaylorHere/BatchScript.git && cd BatchScript && pip3 install -e .
# and you can test it
$> cd BatchScript && python3 test.py
~~~

~~~python
from master import Master
from worker import Worker
import helper 
import os

class Config():

	MaxWorkerSize = os.cpu_count() - 1  #worker数量

	MaxThreadPoolSize = 1024  #每个worker的线程池大小

	ThreadQueueWaitTimeout = 0.01  #worker在job队列上获取数据的超时, 超时后会立即开始批量线程提交

	WorkerGetBatchSize = MaxThreadPoolSize  #额定批大小, 如果worker获取数据时不超时, 那么在获取都这个数量后便开始批量线程提交

	JobsResultsQueueNum = MaxWorkerSize #jobs 和 results 队列对的数量, 该数量如果小于worker数量, 则最后一对会被未分配的worker共用, 共用队列可能会导致锁操作增加

	ResultsBatch = True #将一个batch的所有result当作一个result放入result 队列中

master = Master(func=helper.sleep, config=Config())
master.start()
for i in range(1000):
    master.job_put(0.01)

while True:
    print(master.result().get())
~~~

链接多个 master
~~~python
from master import Master
from worker import Worker
import helper 

master = Master(func=helper.sleep)
master.start()

for i in range(1000):
    master.job_put(0.01)

another_master = Master(func=print, connection=master)#该master会将connection的master的results队列作为jobs队列, 如果该master的队列对比链接master的队列对数量少, 会造成链接master的result不能被全部消耗
another_master.start()

~~~

采用 多进程启动Worker, worker维护线程池运行函数的方案
master内建和worker关联的多个任务队列和对应的多个结果队列
worker按batch从任务队列中获取数据并使用线程池提交运行
批量结束后将任务结果put到结果队列

你可以在config中调整
~~~python
import os

MaxWorkerSize = os.cpu_count() - 1  #worker数量

MaxThreadPoolSize = 1024  #每个worker的线程池大小

ThreadQueueWaitTimeout = 0.01  #worker在job队列上获取数据的超时, 超时后会立即开始批量线程提交

WorkerGetBatchSize = MaxThreadPoolSize  #额定批大小, 如果worker获取数据时不超时, 那么在获取都这个数量后便开始批量线程提交

JobsResultsQueueNum = MaxWorkerSize #jobs 和 results 队列对的数量, 该数量如果小于worker数量, 则最后一对会被未分配的worker共用, 共用队列可能会导致锁操作增加

ResultsBatch = True #将一个batch的所有result当作一个result放入result 队列中
~~~