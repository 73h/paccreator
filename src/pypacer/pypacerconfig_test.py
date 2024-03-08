import unittest

from pypacer.pypacerconfig import PyPacerConfig


class TestPyPacerConfig(unittest.TestCase):

    def test_wrong_default_proxy(self):
        config = {"proxies": {"DIRECT": {"route": "DIRECT"}}, "default": "PROXY_B", "routings": []}
        config = PyPacerConfig(**config)
        with self.assertRaises(ValueError) as err:
            config.validate()
        self.assertEqual(str(err.exception), "default is not in proxies")

    def test_proxy_has_no_route(self):
        config = {"proxies": {"DIRECT": {"route": ""}}, "default": "DIRECT", "routings": []}
        config = PyPacerConfig(**config)
        with self.assertRaises(ValueError) as err:
            config.validate()
        self.assertEqual(str(err.exception), "proxy DIRECT has no route")
