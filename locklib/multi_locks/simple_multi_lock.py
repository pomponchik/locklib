from locklib import LockProtocol


class MultiLock:
    def __init__(self, *locks: LockProtocol) -> None:
        self.locks = locks
