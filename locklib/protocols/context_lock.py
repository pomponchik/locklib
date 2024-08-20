from typing import Type, Optional, Any
from types import TracebackType

try:
    from typing import Protocol, runtime_checkable
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol, runtime_checkable  # type: ignore[assignment]

from locklib.protocols.lock import LockProtocol


@runtime_checkable
class ContextLockProtocol(LockProtocol, Protocol):
    def __enter__(self) -> Any:
        raise NotImplementedError('Do not use the protocol as a lock.')
        return None  # pragma: no cover

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException], traceback: Optional[TracebackType]) -> Any:
        raise NotImplementedError('Do not use the protocol as a lock.')
        return None  # pragma: no cover
