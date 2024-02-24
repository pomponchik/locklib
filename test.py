from locklib.protocols.context_lock import ContextLockProtocol
from threading import Lock
from multiprocessing import Lock as MLock


print(isinstance(Lock(), ContextLockProtocol))
print(isinstance(MLock(), ContextLockProtocol))
