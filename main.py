from threading import Thread, RLock, get_ident
import threading


class SequenceAgent:
    def __init__(self, id, parent, sequence):
        self.id = id

        self.parent = parent

        self.width = sequence.width
        self.current_value = parent.get_new_start()
        self.max_value = self.current_value + self.width

    def get_value(self):
        if self.current_value > self.max_value:
            self.current_value = parent.get_new_start()
            self.max_value = self.current_value + self.width
        return self.current_value

class MiddleSequence:
    def __init__(self, sequence, parent, width, height):
        if width < 2:
            raise ValueError('The branchiness of the tree cannot be less than 2.')

        self.lock = RLock()

        self.sequence = sequence
        self.parent = parent
        self.childs = []

        self.width = width
        self.height = height

        self.is_root = False

    def set_root(self, flag):
        self.is_root = flag

    def get_new_middle(self, width):
        with self.lock:
            if len(self.childs) < self.width:
                new_middle = MiddleSequence(self.sequence, self, width, self.height - 1)
                self.register_child(new_middle, None)
                return new_middle
            else:
                brother = self.parent.get_new_middle(self.width)
                return brother.get_new_middle(width)

    def register_child(self, child, id):
        with self.lock:
            if len(self.childs) < self.width:
                self.childs.append(child)
            else:
                new_middle = self.parent.get_new_middle(self.width)
                new_middle.register_child(child, id)

    def create_agent(self, id):
        with self.lock:
            if self.height == 1:
                agent = SequenceAgent(id, self, self.sequence)
                self.register_child(agent, id)
                return agent
            else:
                self.childs[-1].create_agent(id)

    def register_parent(self, parent):
        with self.lock:
            self.parent = parent

    def get_new_start(self):
        with self.lock:
            pass


class Sequence:
    def __init__(self, width, start=0):
        self.lock = RLock()

        self.root = MiddleSequence(self, self, width, 1)
        self.root.set_root(True)
        self.leaves = {}

        self.width = width

    def create_agent(self, id):
        self.root.create_agent(id)

    def register_child(self, child, id):
        self.leaves[id] = child

    def get_agent(self, id):
        with self.lock:
            if id in self.leaves:
                return leaves[id]
            agent = self.create_agent(id)
            self.register_child(agent, id)
            return agent

    def get_new_middle(self):
        with self.lock:
            new_root = MiddleSeries(self, self, self.root.width * self.width, self.root.height + 1)
            new_root.register_child(self.root, None)

            self.root.set_root(False)
            new_root.set_root(True)

            self.root = new_root

            return self.root.get_new_middle(self.root.width)

seq = Sequence(10)
data = set()
number_of_threads = 1000
numbers_per_thread = 10000

def func():
    agent = seq.get_agent(get_ident())
    for _ in range(numbers_per_thread):
        data.add(agent.get_value())

threads = [Thread(target=func, args=()) for _ in range(number_of_threads)]

for thread in threads:
    thread.start()
for thread in threads:
    thread.loin()

print(len(data))
