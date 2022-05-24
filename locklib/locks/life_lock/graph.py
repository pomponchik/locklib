from threading import Lock
from collections import defaultdict

from locklib.errors import DeadLockError


class LocksGraph:
    def __init__(self):
        self.links = defaultdict(set)
        self.lock = Lock()

    def add_link(self, _from, to):
        cycle_with = self.search_cycles(to, _from)
        if cycle_with is not None:
            if len(cycle_with) > 2:
                cycle_with.reverse()
                cycle_with = ', '.join([str(x) for x in cycle_with])
                message_tail = f' The full path of the cycle: {cycle_with}.'
            else:
                message_tail = ''
            raise DeadLockError(f'A cycle between {_from}th and {to}th threads has been detected.{message_tail}')
        self.links[_from].add(to)

    def delete_link(self, _from, to):
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

        path.pop()

    def search_cycles(self, _from, to):
        return self.dfs_search([], _from, to)
