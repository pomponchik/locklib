from threading import Lock, get_native_id
from collections import deque

from locklib.locks.life_lock.graph import LocksGraph


graph = LocksGraph()

class LifeLock:
    def __init__(self):
        self.lock = Lock()
        self.deque = deque()
        self.local_locks = {}

    def acquire(self):
        id = get_native_id()

        with self.lock:
            self.deque.appendleft(id)

            self.local_locks[id] = Lock()

            if len(self.deque) > 1:
                next = self.deque[1]
                graph.add_link(id, next)
                self.local_locks[next].acquire()

    def release(self):
        id = get_native_id()

        with self.lock:
            self.deque.pop()

            if len(self.deque) >= 1:
                next = self.deque[-1]
                graph.delete_link(next, id)
                self.local_locks[id].release()
            
            del self.local_locks[id]

    def __enter__(self):
        self.acquire()

    def __exit__(self, exception_type, exception_value, traceback):
        self.release()
