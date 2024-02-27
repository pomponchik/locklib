from multiprocessing import Lock as MLock
from threading import Lock as TLock, RLock as TRLock
from asyncio import Lock as ALock

import pytest
import full_match

from locklib import LockProtocol, SmartLock


@pytest.mark.parametrize(
    'lock',
    [
        MLock(),
        TLock(),
        TRLock(),
        ALock(),
        SmartLock(),
    ],
)
def test_locks_are_instances_of_lock_protocol(lock):
    assert isinstance(lock, LockProtocol)


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
def test_other_objects_are_not_instances_of_lock(other):
    assert not isinstance(other, LockProtocol)


def test_not_implemented_methods_for_lock_protocol():
    class LockProtocolImplementation(LockProtocol):
        pass

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        LockProtocolImplementation().acquire()

    with pytest.raises(NotImplementedError, match=full_match('Do not use the protocol as a lock.')):
        LockProtocolImplementation().release()
