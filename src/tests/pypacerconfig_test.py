import unittest

from pypacer.pypacerconfig import PyPacerConfig


class TestPyPacerConfig(unittest.TestCase):

    def test_proxy_has_no_route(self):
        config = {"proxies": {"direct": {"route": "", "default": True}}}
        config = PyPacerConfig(**config)
        with self.assertRaises(ValueError) as err:
            config.validate()
        self.assertEqual(str(err.exception), "proxy direct has no route")

    def test_get_default_proxy_route(self):
        config = {"proxies": {"foo": {"route": "foo"}, "bar": {"route": "bar", "default": True}}}
        config = PyPacerConfig(**config)
        self.assertEqual(config.get_default_proxy().route, "bar")

    def test_get_default_proxy_route_with_no_default_proxy(self):
        config = {"proxies": {"foo": {"route": "foo"}, "bar": {"route": "bar"}}}
        config = PyPacerConfig(**config)
        self.assertEqual(config.get_default_proxy().route, "foo")

    def test_target_is_string(self):
        config = {"proxies": {"foo": {"route": "foo", "targets": [10., "foo"], "default": True}}}
        PyPacerConfig(**config)
