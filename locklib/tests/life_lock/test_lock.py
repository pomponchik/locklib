from queue import Queue
from threading import Thread

import pytest

from locklib.locks.life_lock.lock import LifeLock
from locklib.errors import DeadLockError


def test_raise_when_deadlock():
    number_of_attempts = 20

    lock_1 = LifeLock()
    lock_2 = LifeLock()

    queue = Queue()

    for _ in range(number_of_attempts):
        def function_1():
            try:
                while True:
                    with lock_1:
                        with lock_2:
                            pass
            except DeadLockError as e:
                queue.put(True)

        def function_2():
            try:
                while True:
                    with lock_2:
                        with lock_1:
                            pass
            except DeadLockError as e:
                queue.put(True)


        thread_1 = Thread(target=function_1)
        thread_2 = Thread(target=function_2)
        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()

        assert queue.get()
