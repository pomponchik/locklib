try:
    from typing import Protocol, runtime_checkable
except ImportError:  # pragma: no cover
    from typing_extensions import Protocol, runtime_checkable  # type: ignore[assignment]

from typing import Any

@runtime_checkable
class LockProtocol(Protocol):
    def acquire(self) -> Any:
        return None

    def release(self) -> Any:
        return None
