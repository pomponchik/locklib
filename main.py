from threading import Thread
from locklib import LifeLock


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
