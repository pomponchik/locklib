from time import sleep
from queue import Queue
from threading import Thread, Lock

import pytest

from locklib.locks.life_lock.lock import SmartLock
from locklib.errors import DeadLockError


def test_release_unlocked():
    lock = SmartLock()

    with pytest.raises(RuntimeError):
        lock.release()


def test_normal_using():
    number_of_threads = 5
    number_of_attempts_per_thread = 100000

    lock = SmartLock()
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

    lock_1 = SmartLock()
    lock_2 = SmartLock()

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


@pytest.mark.timeout(1)
def test_raise_when_not_so_simple_deadlock():
    number_of_attempts = 50

    lock_1 = SmartLock()
    lock_2 = SmartLock()
    lock_3 = SmartLock()

    queue = Queue()

    for _ in range(number_of_attempts):
        flag = False
        cycles = 0
        lock = Lock()
        def function_1():
            nonlocal flag
            nonlocal cycles
            try:
                while True:
                    with lock_1:
                        sleep(0.0001)
                        with lock_2:
                            sleep(0.0001)
                            with lock_3:
                                if flag:
                                    break
            except DeadLockError as e:
                with lock:
                    cycles += 1
                    if cycles == 2:
                        flag = True
                queue.put(True)
                raise e

        def function_2():
            nonlocal flag
            nonlocal cycles
            try:
                while True:
                    with lock_2:
                        sleep(0.0001)
                        with lock_3:
                            sleep(0.0001)
                            with lock_1:
                                if flag:
                                    break
            except DeadLockError as e:
                with lock:
                    cycles += 1
                    if cycles == 2:
                        flag = True
                queue.put(True)
                raise e

        def function_3():
            nonlocal flag
            nonlocal cycles
            try:
                while True:
                    with lock_3:
                        sleep(0.0001)
                        with lock_1:
                            sleep(0.0001)
                            with lock_2:
                                if flag:
                                    break
            except DeadLockError as e:
                with lock:
                    cycles += 1
                    if cycles == 2:
                        flag = True
                queue.put(True)
                raise e


        thread_1 = Thread(target=function_1)
        thread_2 = Thread(target=function_2)
        thread_3 = Thread(target=function_3)
        thread_1.start()
        thread_2.start()
        thread_3.start()

        thread_1.join()
        thread_2.join()
        thread_3.join()

        counter = 0

        for _ in range(2):
            queue.get()
            counter += 1

        assert counter == 2
