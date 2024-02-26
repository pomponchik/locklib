from multiprocessing import Lock as MLock
from threading import Lock as TLock, RLock as TRLock
from asyncio import Lock as ALock

import pytest

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
        ALock(),  # asyncio lock is an instance of the AsyncContextLockProtocol, not just ContextLockProtocol.
    ],
)
def test_other_objects_are_not_instances_of_context_lock(other):
    assert not isinstance(other, ContextLockProtocol)
