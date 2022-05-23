from threading import Thread
from locklib import LifeLock, DeadLockError


lock_1 = LifeLock()
lock_2 = LifeLock()

flag = False

def time():
    global flag
    try:
        while True:
            with lock_1:
                with lock_2:
                    if flag:
                        break
    except DeadLockError as e:
        flag = True
        raise e

def space():
    global flag
    try:
        while True:
            with lock_2:
                with lock_1:
                    if flag:
                        break
    except DeadLockError as e:
        flag = True
        raise e


t1 = Thread(target=time)
t2 = Thread(target=space)
t1.start()
t2.start()
