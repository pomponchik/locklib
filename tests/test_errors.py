import pytest

from locklib.errors import DeadLockError


def test_raise():
    with pytest.raises(DeadLockError):
        raise DeadLockError()
