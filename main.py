from threading import Thread, Lock, get_native_id
from collections import defaultdict


class DeadLockError(ValueError):
    pass

class LocksGraph:
    def __init__(self):
        self.links = defaultdict(set)
        self.lock = Lock()

    def add_link(self, from, to):
        with self.lock:
            cycle_with = self.search_cycles(to, from)
            if cycle_with is not None:
                cycle_with = ', '.join(cycle_with)
                raise DeadLockError(f'A cycle between {from} and {to} has been detected. The full path of the cycle: {cycle_with}.')
            self.links[from].add(to)

    def delete_link(self, from, to):
        with self.lock:
            if from in self.links:
                del self.links[from][to]
                if not self.links[from]:
                    del self.links[from]

    def get_links_from(self, from):
        return self.links[from]

    def dfs_search(self, path, current_node, target):
        path.append(current_node)

        neighbors = self.get_links_from(current_node)

        if neighbors:
            for link in neighbors:
                if link == target:
                    return path
                result_of_next_search = self.dfs_search(path, link, target)
                if result_of_next_search is not None:
                    return result_of_next_search

    def search_cycles(self, from, to):
        return self.dfs_search([], from, to)

graph = LocksGraph()

class LifeLock:
    def __init__(self):
        self.lock = Lock()

    def acquire(self):
        pass

    def release(self):
        pass
