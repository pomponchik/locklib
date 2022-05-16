from threading import Thread, RLock, get_ident, get_native_id
import threading

class LockIntersectionError(ValueError):
    pass

class SequenceAgent:
    def __init__(self, id, parent, sequence):
        self.lock = RLock()
        self.id = id

        self.parent = parent

        self.width = sequence.width

        self.current_value = parent.get_new_start(self.width)
        self.max_value = self.current_value + self.width

    def get_value(self):
        print('pre 1')
        with self.lock:
            if self.current_value > self.max_value:
                while True:
                    try:
                        self.current_value = self.parent.get_new_start(self.width)
                        break
                    except LockIntersectionError as e:
                        pass
                self.max_value = self.current_value + self.width
            result = self.current_value
            self.current_value += 1
            return result

class MiddleSequence:
    def __init__(self, sequence, parent, width, height, is_root):
        if width < 2:
            raise ValueError('The branchiness of the tree cannot be less than 2.')

        self.lock = RLock()

        self.sequence = sequence
        self.parent = parent
        self.childs = []

        self.width = width
        self.height = height

        self.is_root = is_root

        if not self.is_root:
            self.current_value = parent.get_new_start(self.width)
        else:
            self.current_value = self.sequence.start
        self.max_value = self.current_value + self.width

    def set_root(self, flag):
        print('pre 2')
        with self.lock:
            self.is_root = flag

    def get_new_middle(self, width):
        print('pre 3')
        with self.lock:
            if len(self.childs) < self.width:
                new_middle = MiddleSequence(self.sequence, self, width, self.height - 1, False)
                self.register_child(new_middle, None)
                return new_middle
            else:
                brother = self.parent.get_new_middle(self.width)
                return brother.get_new_middle(width)

    def register_child(self, child, id):
        print('pre 4')
        with self.lock:
            if len(self.childs) < self.width:
                self.childs.append(child)
            else:
                new_middle = self.parent.get_new_middle(self.width)
                new_middle.register_child(child, id)

    def create_agent(self, id):
        print('pre 5')
        with self.lock:
            if self.height == 1:
                agent = SequenceAgent(id, self, self.sequence)
                self.register_child(agent, id)
                return agent
            else:
                return self.childs[-1].create_agent(id)

    def register_parent(self, parent):
        print('pre 6')
        with self.lock:
            self.parent = parent

    def get_new_start(self, width):
        print('pre 7')
        locked = self.lock.acquire(blocking=False)
        if not locked:
            raise LockIntersectionError('Locks are intersected.')
        with self.lock:
            if self.is_root:
                result = self.current_value
                self.current_value += width
                self.max_value = self.current_value
            else:
                if self.current_value > self.max_value:
                    print(self.is_root)
                    self.current_value = self.parent.get_new_start(self.width)
                    self.max_value = self.current_value + self.width
                result = self.current_value
                self.current_value += width
            return result

class Sequence:
    def __init__(self, width, start=0):
        self.lock = RLock()

        self.width = width

        self.start = start

        self.root = MiddleSequence(self, self, width, 1, True)
        self.root.set_root(True)
        self.leaves = {}

    def create_agent(self, id):
        print('pre 8')
        with self.lock:
            return self.root.create_agent(id)

    def register_child(self, child, id):
        print('pre 9')
        with self.lock:
            self.leaves[id] = child

    def get_agent(self, id):
        print('pre 10')
        with self.lock:
            print('post 10')
            if id in self.leaves:
                return self.leaves[id]
            agent = self.create_agent(id)
            self.register_child(agent, id)
            return agent

    def get_new_middle(self, width):
        print('pre 11')
        with self.lock:
            new_root = MiddleSequence(self, self, self.root.width * self.width, self.root.height + 1, True)
            new_root.current_value = self.root.current_value
            new_root.register_child(self.root, None)

            self.root.set_root(False)
            self.root.parent = new_root

            self.root = new_root

            return self.root.get_new_middle(self.root.width)

seq = Sequence(10)
data = set()
data2 = []
number_of_threads = 1000
numbers_per_thread = 10000
rs = set()
kek = set()

def func():
    kek.add(get_native_id())
    agent = seq.get_agent(get_native_id())
    for _ in range(numbers_per_thread):
        value = agent.get_value()
        data.add(value)
        print(value)
        #data2.append(value)
        #rs.add(agent.parent.sequence.root.is_root)
    #"""

threads = [Thread(target=func, args=()) for _ in range(number_of_threads)]


for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print(len(data))
print(len(data2))
print(rs)
print(len(seq.leaves))
print('len threads:', len(threads))

"""
k = set()
r = []
for n in data2:
    if n in k:
        r.append(n)
    k.add(n)

"""
#print(r)
