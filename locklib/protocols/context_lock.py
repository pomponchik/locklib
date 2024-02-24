from typing import Type, Optional, Any
from types import TracebackType

try:
    from typing import Protocol, runtime_checkable
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol, runtime_checkable  # type: ignore[assignment]


@runtime_checkable
class ContextLockProtocol(Protocol):
    def __enter__(self) -> Any:
        raise NotImplementedError('Do not use the protocol as a lock.')

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:
        raise NotImplementedError('Do not use the protocol as a lock.')

    def acquire(self) -> None:
        raise NotImplementedError('Do not use the protocol as a lock.')

    def release(self) -> None:
        raise NotImplementedError('Do not use the protocol as a lock.')
