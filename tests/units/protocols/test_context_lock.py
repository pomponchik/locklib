import sys
from multiprocessing import Lock as MLock
from threading import Lock as TLock, RLock as TRLock
from asyncio import Lock as ALock
from contextlib import contextmanager

import pytest
import full_match

from locklib import ContextLockProtocol, SmartLock


@pytest.mark.parametrize(
    'lock',
    [
        MLock(),
        TLock(),
        TRLock(),
        SmartLock(),
    ],
)
def test_locks_are_instances_of_context_lock_protocol(lock):
    assert isinstance(lock, ContextLockProtocol)


@pytest.mark.parametrize(
    'other',
    [
        1,
        None,
        'kek',
        'lock',
        [],
        {},
    ],
)
def test_other_objects_are_not_instances_of_context_lock(other):
    assert not isinstance(other, ContextLockProtocol)


@pytest.mark.skipif(sys.version_info < (3, 9) and sys.version_info > (3, 7), reason='Problems with Python 3.8')
def test_asyncio_lock_is_not_just_context_lock():
    """
    asyncio lock is an instance of the AsyncContextLockProtocol, not just ContextLockProtocol.
    But! In python 3.8 it is both.
    """
    print(sys.version_info)
    assert not isinstance(ALock(), ContextLockProtocol)


def test_just_contextmanager_is_not_context_lock():
    @contextmanager
    def context_manager():
        yield 'kek'

    assert not isinstance(context_manager(), ContextLockProtocol)


def test_not_implemented_methods_for_context_lock_protocol():
    class ContextLockProtocolImplementation(ContextLockProtocol):
        pass

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        ContextLockProtocolImplementation().acquire()

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        ContextLockProtocolImplementation().release()

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        ContextLockProtocolImplementation().__enter__()

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        ContextLockProtocolImplementation().__exit__(None, None, None)


def tests_for_type_checking():
    def some_function(lock: ContextLockProtocol) -> ContextLockProtocol:
        return lock

    some_function(MLock())
    some_function(TLock())
    some_function(TRLock())
    some_function(SmartLock())
