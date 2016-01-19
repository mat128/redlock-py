import unittest
import time
from hamcrest import assert_that, is_, greater_than_or_equal_to
import mock
from redlock.failfast import RedlockFailFast
import test_redlock


class RedlockFailFastTest(unittest.TestCase):
    @mock.patch('redis.StrictRedis', new=test_redlock.FakeRedisCustom)
    def test_auto_extend(self):
        self.redlock = RedlockFailFast([{'host': 'localhost', 'db': 'mytest'}], autoextend_every_ms=100)
        lock = self.redlock.lock(resource='test', ttl=500)
        time.sleep(1)

        for server in self.redlock.servers:
            assert_that(server.pttl('test'), is_(greater_than_or_equal_to(500-100)))

        self.redlock.unlock(lock)