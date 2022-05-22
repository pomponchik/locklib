from threading import Thread, Lock, get_native_id
from collections import defaultdict, deque


class DeadLockError(ValueError):
    pass

class LocksGraph:
    def __init__(self):
        self.links = defaultdict(set)
        self.lock = Lock()

    def add_link(self, _from, to):
        with self.lock:
            cycle_with = self.search_cycles(to, _from)
            if cycle_with is not None:
                cycle_with = ', '.join([str(x) for x in cycle_with])
                raise DeadLockError(f'A cycle between {_from} and {to} has been detected. The full path of the cycle: {cycle_with}.')
            self.links[_from].add(to)

    def delete_link(self, _from, to):
        with self.lock:
            if _from in self.links:
                if to in self.links[_from]:
                    self.links[_from].remove(to)
                if not self.links[_from]:
                    del self.links[_from]

    def get_links_from(self, _from):
        return self.links[_from]

    def dfs_search(self, path, current_node, target):
        path.append(current_node)

        neighbors = self.get_links_from(current_node)

        if neighbors:
            for link in neighbors:
                if link == target:
                    path.append(target)
                    return path
                result_of_next_search = self.dfs_search(path, link, target)
                if result_of_next_search is not None:
                    return result_of_next_search

    def search_cycles(self, _from, to):
        return self.dfs_search([], _from, to)

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



lock_1 = LifeLock()
lock_2 = LifeLock()


def time():
        while True:
            with lock_1:
                with lock_2:
                    pass

def space():
        while True:
            with lock_2:
                with lock_1:
                    pass


t1 = Thread(target=time)


t2 = Thread(target=space)


t1.start()
t2.start()
