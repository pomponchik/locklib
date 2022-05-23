from queue import Queue
from threading import Thread

import pytest

from locklib.locks.life_lock.lock import LifeLock
from locklib.errors import DeadLockError


def test_release_unlocked():
    lock = LifeLock()

    with pytest.raises(RuntimeError):
        lock.release()


def test_normal_using():
    number_of_threads = 5
    number_of_attempts_per_thread = 100000

    lock = LifeLock()
    index = 0

    def function():
        nonlocal index

        for _ in range(number_of_attempts_per_thread):
            with lock:
                index += 1

    threads = [Thread(target=function) for _ in range(number_of_threads)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert index == number_of_threads * number_of_attempts_per_thread


@pytest.mark.timeout(1)
def test_raise_when_simple_deadlock():
    number_of_attempts = 50

    lock_1 = LifeLock()
    lock_2 = LifeLock()

    queue = Queue()

    for _ in range(number_of_attempts):
        flag = False
        def function_1():
            nonlocal flag
            try:
                while True:
                    with lock_1:
                        with lock_2:
                            if flag:
                                break
            except DeadLockError as e:
                flag = True
                queue.put(True)
                raise e

        def function_2():
            nonlocal flag
            try:
                while True:
                    with lock_2:
                        with lock_1:
                            if flag:
                                break
            except DeadLockError as e:
                flag = True
                queue.put(True)
                raise e


        thread_1 = Thread(target=function_1)
        thread_2 = Thread(target=function_2)
        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()

        assert queue.get()
