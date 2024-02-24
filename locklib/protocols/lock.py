try:
    from typing import Protocol, runtime_checkable
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol, runtime_checkable  # type: ignore[assignment]


@runtime_checkable
class LockProtocol(Protocol):
    def acquire(self) -> None:
        raise NotImplementedError('Do not use the protocol as a lock.')

    def release(self) -> None:
        raise NotImplementedError('Do not use the protocol as a lock.')
