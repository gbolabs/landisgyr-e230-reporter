from os import error
from typing import NoReturn
import measureobject


DATABASE_FILE = "missed-queue.pickledb.data"
MISSING_QUEUE_LIST = "missed-azure-uploads"


def get_datbase():
    import pickledb
    db = pickledb.load(DATABASE_FILE, False)

    if not db.lexists(MISSING_QUEUE_LIST):
        db.lcreate(MISSING_QUEUE_LIST)

    return db


def enqueue_measure(jsondata):
    db = get_datbase()
    if not db.ladd(MISSING_QUEUE_LIST, jsondata):
        print('Unable to queue missing upload')


def pop_measure():
    db = get_datbase()
    length = db.llen(MISSING_QUEUE_LIST)
    if length > 0:
        measure = (measureobject.Measure) (db.lget(MISSING_QUEUE_LIST, 0))
        return measure
    else:
        print('queue is empty, return nothing')
        pass


def dequeue_measure(pos=0):
    db = get_datbase()
    length = db.llen(MISSING_QUEUE_LIST)
    if length > 0 & length > pos:
        
    else:
        pass
