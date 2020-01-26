import os

MaxWorkerSize = os.cpu_count() - 1  #worker数量

MaxThreadPoolSize = 1024  #每个worker的线程池大小

ThreadQueueWaitTimeout = 0.01  #worker在job队列上获取数据的超时, 超时后会立即开始批量线程提交

WorkerGetBatchSize = MaxThreadPoolSize  #额定批大小, 如果worker获取数据时不超时, 那么在获取都这个数量后便开始批量线程提交

JobsResultsQueueNum = MaxWorkerSize #jobs 和 results 队列对的数量, 该数量如果小于worker数量, 则最后一对会被未分配的worker共用, 共用队列可能会导致锁操作增加

ResultsBatchSize = 1024 #对结果重新打batch, 如果值为0, 则result不打batch