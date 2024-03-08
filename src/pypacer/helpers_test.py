import unittest

from pypacer.helpers import get_target_type, sort_by_rating
from pypacer.pypacerconfig import PyPacerConfig


class TestHelpers(unittest.TestCase):

    def test_target_type_ip_mask(self):
        self.assertEqual(get_target_type("127.0.0.0/24"), "IP_MASK")

    def test_target_type_ip(self):
        self.assertEqual(get_target_type("127.0.0.1"), "IP")

    def test_target_type_hosts(self):
        self.assertEqual(get_target_type(".example.com"), "HOSTS")

    def test_target_type_host(self):
        self.assertEqual(get_target_type("example.com"), "HOST")

    def test_sort_by_rating(self):
        config = {"proxies": {"A": {"route": "A", "targets": [".example.com"]},
                              "B": {"route": "B", "targets": ["foo.example.com"]}}, "default": "A"}
        config = PyPacerConfig(**config)
        config.validate()
        proxies = [p for p in config.proxies.values()]
        self.assertEqual(proxies[0].route, "A")
        self.assertEqual(proxies[0].targets[0].rating, 1)
        proxies.sort(key=sort_by_rating)
        self.assertEqual(proxies[0].route, "B")
