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
        previous_element_lock = None

        with self.lock:
            with graph.lock:
                if not len(self.deque):
                    self.deque.appendleft(id)
                    self.local_locks[id] = Lock()
                    self.local_locks[id].acquire()
                else:
                    previous_element = self.deque[0]
                    graph.add_link(id, previous_element)
                    self.deque.appendleft(id)
                    self.local_locks[id] = Lock()
                    self.local_locks[id].acquire()
                    previous_element_lock = self.local_locks[previous_element]

        if previous_element_lock is not None:
            previous_element_lock.acquire()


    def release(self):
        id = get_native_id()

        with self.lock:
            with graph.lock:
                if id not in self.local_locks:
                    raise RuntimeError('Release unlocked lock.')
                if len(self.deque) == 1:
                    self.deque.pop()
                    lock = self.local_locks[id]
                    del self.local_locks[id]
                    lock.release()
                else:
                    self.deque.pop()
                    lock = self.local_locks[id]
                    del self.local_locks[id]
                    next_element = self.deque[-1]
                    graph.delete_link(next_element, id)
                    lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exception_type, exception_value, traceback):
        self.release()
