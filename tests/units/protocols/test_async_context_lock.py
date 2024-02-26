from multiprocessing import Lock as MLock
from threading import Lock as TLock, RLock as TRLock
from asyncio import Lock as ALock
from contextlib import asynccontextmanager

import pytest
import full_match

from locklib import AsyncContextLockProtocol, SmartLock


@pytest.mark.parametrize(
    'lock',
    [
        ALock(),
    ],
)
def test_locks_are_instances_of_context_lock_protocol(lock):
    assert isinstance(lock, AsyncContextLockProtocol)


@pytest.mark.parametrize(
    'other',
    [
        1,
        None,
        'kek',
        'lock',
        [],
        {},
        MLock(),
        TLock(),
        TRLock(),
        SmartLock(),
    ],
)
def test_other_objects_are_not_instances_of_context_lock(other):
    assert not isinstance(other, AsyncContextLockProtocol)


def test_just_async_contextmanager_is_not_async_context_lock():
    @asynccontextmanager
    async def context_manager():
        yield 'kek'

    assert not isinstance(context_manager(), AsyncContextLockProtocol)


def test_not_implemented_methods_for_async_context_lock_protocol():
    class AsyncContextLockProtocolImplementation(AsyncContextLockProtocol):
        pass

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        AsyncContextLockProtocolImplementation().acquire()

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        AsyncContextLockProtocolImplementation().release()

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        AsyncContextLockProtocolImplementation().__aenter__()

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        AsyncContextLockProtocolImplementation().__aexit__(None, None, None)
