from mock import patch
from redlock.fifo import RedlockFIFO
import test_redlock


class RedlockFIFOTest(test_redlock.RedlockTest):
    @patch('redis.StrictRedis', new=test_redlock.FakeRedisCustom)
    def setUp(self):
        self.redlock = RedlockFIFO(test_redlock.get_servers_pool(active=1, inactive=0))
        self.redlock_with_51_servers_up_49_down = RedlockFIFO(test_redlock.get_servers_pool(active=51, inactive=49))
        self.redlock_with_50_servers_up_50_down = RedlockFIFO(test_redlock.get_servers_pool(active=50, inactive=50))

    def test_calls_are_handled_in_order(self):
        pass