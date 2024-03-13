import unittest

from pypacer.helpers import get_target_type, sort_by_rating, is_ipaddress, is_network, \
    is_hostname
from pypacer.pypacerconfig import PyPacerConfig


class TestHelpers(unittest.TestCase):

    def test_is_ipaddress(self):
        self.assertTrue(is_ipaddress("10.11.12.13"))
        self.assertFalse(is_ipaddress("10.11.12.13.14"))
        self.assertFalse(is_ipaddress("example.com"))
        self.assertTrue(is_ipaddress("2001:0db8:85a3:08d3:1319:8a2e:0370:7344"))

    def test_is_network(self):
        self.assertTrue(is_network("10.11.12.13/32"))
        self.assertFalse(is_network("10.11.12.13.14"))
        self.assertFalse(is_network("example.com"))
        self.assertTrue(is_network("2001:0db8:85a3:08d3::/64"))

    def test_target_type_ip_mask(self):
        self.assertEqual(get_target_type("127.0.0.0/24"), "NETWORK")

    def test_target_type_ip(self):
        self.assertEqual(get_target_type("127.0.0.1"), "IP")

    def test_target_type_hosts(self):
        self.assertEqual(get_target_type(".example.com"), "HOSTS")

    def test_target_type_host(self):
        self.assertEqual(get_target_type("example.com"), "HOST")
        self.assertEqual(get_target_type("example.com."), "HOST")

    def test_target_type_string_l(self):
        self.assertEqual(get_target_type("10."), "STRING_L")

    def test_target_type_string_r(self):
        self.assertEqual(get_target_type(".102.123"), "STRING_R")

    def test_target_type_string(self):
        self.assertEqual(get_target_type("10"), "STRING")

    def test_is_hostname(self):
        self.assertTrue(is_hostname("example.com"))
        self.assertTrue(is_hostname("foo.example.com"))
        self.assertTrue(is_hostname("foo.bar.example"))
        self.assertTrue(is_hostname("test-123.foo.bar.example-de"))
        self.assertTrue(is_hostname("exämple.com"))
        self.assertTrue(is_hostname(".exämple.com"))
        self.assertTrue(is_hostname(".exämple.com."))
        self.assertTrue(is_hostname("exämple.com."))

    def test_sort_by_rating(self):
        config = {"proxies": {"A": {"route": "A", "default": True, "targets": [".example.com"]},
                              "B": {"route": "B", "targets": ["foo.example.com"]}}}
        config = PyPacerConfig(**config)
        config.recognize_overlaps()
        proxies = [p for p in config.proxies.values()]
        self.assertEqual(proxies[0].route, "A")
        self.assertEqual(proxies[1].targets[0].rating, -1)
        proxies.sort(key=sort_by_rating)
        self.assertEqual(proxies[0].route, "B")
