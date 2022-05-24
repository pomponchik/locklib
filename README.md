# locklib


[Deadlocks](https://en.wikipedia.org/wiki/Deadlock) are the most terribly enemies of all programmers who are making multithreaded programs. If you are a one of them - maybe this library is helpful for you.


### How can i use it?

Get the locklib from the [pip](https://pypi.org/project/locklib/):

```
$ pip install locklib
```

And use a lock from this library as a usual [```Lock``` from the standart library](https://docs.python.org/3/library/threading.html#lock-objects):

```python
from threading import Thread
from locklib import LifeLock


lock = LifeLock()
counter = 0

def function():
  global counter

  for _ in range(1000):
      with lock:
          counter += 1

thread_1 = Thread(target=function)
thread_2 = Thread(target=function)
thread_1.start()
thread_2.start()

assert counter == 2000
```

In this case the lock helps to us to not get a race condition, as the standart ```Lock```. But! Let's provoke a deadlock and look what happens:

```python
from threading import Thread
from locklib import LifeLock


lock_1 = LifeLock()
lock_2 = LifeLock()

def function_1():
  while True:
    with lock_1:
      with lock_2:
        pass

def function_2():
  while True:
    with lock_2:
      with lock_1:
        pass

thread_1 = Thread(target=function_1)
thread_2 = Thread(target=function_2)
thread_1.start()
thread_2.start()
```

And... We have an exception like this:

```
...
locklib.errors.DeadLockError: A cycle between 1970256th and 1970257th threads has been detected. The full path of the cycle: 1970257, 1970256.
```

Deadlocks are impossible for this lock!

If you want to catch the exception, import it from the locklib too:

```python
from locklib import DeadLockError
```


### How it works?

Detecting of deadlocks based on [Wait-for Graph](https://en.wikipedia.org/wiki/Wait-for_graph).
