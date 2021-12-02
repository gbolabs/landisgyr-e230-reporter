from typing import Any
import persistqueue
from persistqueue.sqlqueue import FIFOSQLiteQueue

QUEUE_STORAGE = "/home/pi/measure-posting-queue.data"


def queue_measure(jsondata):
    q = build_queue()
    q.put(jsondata)

def dequeue():
    return build_queue().get()


def ack(item):
    build_queue().ack(item)


def nack(item):
    build_queue().nack(item)


def build_queue() -> FIFOSQLiteQueue:
    q = persistqueue.FIFOSQLiteQueue(QUEUE_STORAGE, auto_commit=True)
