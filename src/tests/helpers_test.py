import unittest

from paccreator.helpers import get_target_type, sort_by_rating, is_ipaddress, is_network, \
    is_hostname, TargetType
from paccreator.paccreatorconfig import PacCreatorConfig


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
        self.assertEqual(get_target_type("127.0.0.0/24"), TargetType.NETWORK)

    def test_target_type_ip(self):
        self.assertEqual(get_target_type("127.0.0.1"), TargetType.IP)

    def test_target_type_hosts(self):
        self.assertEqual(get_target_type(".example.com"), TargetType.HOSTS)

    def test_target_type_host(self):
        self.assertEqual(get_target_type("example.com"), TargetType.HOST)
        self.assertEqual(get_target_type("example.com."), TargetType.HOST)

    def test_target_type_string_l(self):
        self.assertEqual(get_target_type("10."), TargetType.STRING_L)

    def test_target_type_string_r(self):
        self.assertEqual(get_target_type(".102.123"), TargetType.STRING_R)

    def test_target_type_string(self):
        self.assertEqual(get_target_type("10"), TargetType.STRING)

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
        config = {"proxies": [{"route": "A", "tags": ["default"], "targets": [".example.com"]},
                              {"route": "B", "targets": ["foo.example.com"]}]}
        config = PacCreatorConfig(**config)
        config.recognize_overlaps()
        self.assertEqual(config.proxies[0].route, "A")
        self.assertEqual(config.proxies[1].targets[0].rating, 1)
        self.assertEqual(config.proxies[0].targets[0].rating, 4)
        config.proxies.sort(key=sort_by_rating)
        self.assertEqual(config.proxies[0].route, "B")

    def test_sort_by_rating_with_plain_hostname_tag(self):
        config = {"proxies": [{"route": "A", "tags": ["catch-plain-hostnames"], "targets": [".example.com"]},
                              {"route": "B", "targets": ["foo.example.com"]}]}
        config = PacCreatorConfig(**config)
        config.recognize_overlaps()
        config.proxies.sort(key=sort_by_rating)
        self.assertEqual(config.proxies[0].route, "B")

    def test_sort_by_rating_with_plain_hostname_tag_in_exclusive_section(self):
        config = {"proxies": [{"route": "A", "tags": ["catch-plain-hostnames"], "targets": []},
                              {"route": "B", "targets": ["foo.example.com"]}]}
        config = PacCreatorConfig(**config)
        config.recognize_overlaps()
        config.proxies.sort(key=sort_by_rating)
        self.assertEqual(config.proxies[0].route, "A")
