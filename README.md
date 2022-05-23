# locklib


Deadlocks are the most terribly enemy of all programmers who are making multithreaded programs. If you are a one of them - maybe this library is helpful for you.

### How can i use it?

Get the locklib from the pip:

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
thread_1.start()

assert counter == 2000
```

In this case the lock helps to us to not get a race condition, as the standart ```Lock```. But!


### How it works?
