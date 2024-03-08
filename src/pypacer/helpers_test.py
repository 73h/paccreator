import unittest

from pypacer.helpers import get_target_type, TargetType


class TestHelpers(unittest.TestCase):

    def test_target_type_ip_mask(self):
        self.assertEqual(get_target_type("127.0.0.0/24"), TargetType.IP_MASK)

    def test_target_type_ip(self):
        self.assertEqual(get_target_type("127.0.0.1"), TargetType.IP)

    def test_target_type_hosts(self):
        self.assertEqual(get_target_type(".example.com"), TargetType.HOSTS)

    def test_target_type_host(self):
        self.assertEqual(get_target_type("example.com"), TargetType.HOST)
