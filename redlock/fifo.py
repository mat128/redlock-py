import threading
from redlock import Redlock


class RedlockFIFO(Redlock):

    def __init__(
            self, connection_list, retry_count=None, retry_delay=None,
            fifo_retry_count=10, fifo_retry_delay=0.2, fifo_queue_length=32
    ):
        super(RedlockFIFO, self).__init__(connection_list, retry_count, retry_delay)
        self.fifo_retry_count = fifo_retry_count
        self.fifo_retry_delay = fifo_retry_delay
        self.fifo_queue_length = fifo_queue_length

    def lock(self, resource, ttl):
        def get_resource_name_with_position(resource, position):
            if position == 0:
                return resource
            else:
                return "{}__{}".format(resource, position)

        current_position = None
        lock = None
        retries = 0

        while current_position is not 0 and retries <= self.fifo_retry_count:
            if current_position is not None:
                next_position = current_position - 1
            else:
                next_position = self.fifo_queue_length

            next_lock = super(RedlockFIFO, self).lock(get_resource_name_with_position(resource, next_position), ttl)
            print '%s - Tried pos %s, got %s' % (threading.current_thread(), next_position, next_lock)

            if next_lock:
                if lock is not None:
                    super(RedlockFIFO, self).unlock(lock)
                current_position = next_position
                lock = next_lock
            else:
                retries += 1

        if current_position == 0:
            return lock
        else:
            return False
