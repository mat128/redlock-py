import time
from redlock import Redlock
import threading

class RedlockFailFast(Redlock):

    def __init__(self, connection_list, retry_count=None, retry_delay=None, autoextend_every_ms=500):
        super(RedlockFailFast, self).__init__(connection_list, retry_count, retry_delay)
        self.autoextend_every_ms = autoextend_every_ms
        self.extend_thread = None

    def lock(self, resource, ttl):
        lock = super(RedlockFailFast, self).lock(resource, ttl)
        def autoextend(redlock, lock, ttl):
            while True:
                redlock.extend(lock=lock, new_ttl=ttl)
                time.sleep(0.1)

        self.extend_thread = threading.Thread(target=autoextend, args=(self, lock, ttl))
        self.extend_thread.start()

        return lock

    def unlock(self, lock):
        self.extend_thread.stop()
        return super(RedlockFailFast, self).unlock(lock)


