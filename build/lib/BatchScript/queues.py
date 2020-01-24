import queue as ThreadQueue
import multiprocessing.Queue as ProcessQueue

from dataclasses import dataclass, field
from typing import Any

from master import Master
from worker import Worker

@dataclass()
class ReportItem:
    item : Any = None

class ReportQueue(ThreadQueue):
    pass

class DoneQueue(ProcessQueue):
    pass



