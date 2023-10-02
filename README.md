![logo](https://raw.githubusercontent.com/pomponchik/locklib/develop/docs/assets/logo_5.png)

[![Downloads](https://static.pepy.tech/badge/locklib/month)](https://pepy.tech/project/locklib)
[![Downloads](https://static.pepy.tech/badge/locklib)](https://pepy.tech/project/locklib)
[![codecov](https://codecov.io/gh/pomponchik/locklib/graph/badge.svg?token=O9G4FD8QFC)](https://codecov.io/gh/pomponchik/locklib)
[![Test-Package](https://github.com/pomponchik/locklib/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/locklib/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/locklib.svg)](https://pypi.python.org/pypi/locklib)
[![PyPI version](https://badge.fury.io/py/locklib.svg)](https://badge.fury.io/py/locklib)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

[Deadlocks](https://en.wikipedia.org/wiki/Deadlock) are the most terrible enemies of all programmers who make multithreaded programs. If you are a one of them - this library is going to help you out.


### How can I use it?

Get the locklib from the [pip](https://pypi.org/project/locklib/):

```
$ pip install locklib
```

And use a lock from this library as a usual [```Lock``` from the standard library](https://docs.python.org/3/library/threading.html#lock-objects):

```python
from threading import Thread
from locklib import SmartLock


lock = SmartLock()
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

In this case the lock helps us not to get a race condition, as the standard ```Lock``` does. But! Let's trigger a deadlock and look what happens:

```python
from threading import Thread
from locklib import SmartLock


lock_1 = SmartLock()
lock_2 = SmartLock()

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
locklib.errors.DeadLockError: A cycle between 1970256th and 1970257th threads has been detected.
```

Deadlocks are impossible for this lock!

If you want to catch the exception, import this from the locklib too:

```python
from locklib import DeadLockError
```


### How does it work?

Deadlock detection based on [Wait-for Graph](https://en.wikipedia.org/wiki/Wait-for_graph).
