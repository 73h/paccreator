import unittest

from pypacer.pypacerconfig import PyPacerConfig


class TestPyPacerConfig(unittest.TestCase):

    def test_wrong_default_proxy(self):
        config = {"proxies": {"DIRECT": {"route": "DIRECT"}}, "default": "PROXY_B"}
        config = PyPacerConfig(**config)
        with self.assertRaises(ValueError) as err:
            config.validate()
        self.assertEqual(str(err.exception), "default is not in proxies")

    def test_proxy_has_no_route(self):
        config = {"proxies": {"DIRECT": {"route": ""}}, "default": "DIRECT"}
        config = PyPacerConfig(**config)
        with self.assertRaises(ValueError) as err:
            config.validate()
        self.assertEqual(str(err.exception), "proxy DIRECT has no route")

    def test_get_default_proxy_route(self):
        config = {"proxies": {"foo": {"route": "foo"}, "bar": {"route": "bar"}}, "default": "bar"}
        config = PyPacerConfig(**config)
        self.assertEqual(config.get_default_proxy_route(), "bar")

    def test_target_is_string(self):
        config = {"proxies": {"foo": {"route": "foo", "targets": [10., "foo"]}}, "default": "foo"}
        PyPacerConfig(**config)
