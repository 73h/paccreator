import unittest

from paccreator.paccreatorconfig import PacCreatorConfig


class TestPacCreatorConfig(unittest.TestCase):

    def test_proxy_has_no_route(self):
        config = {"proxies": [{"route": ""}]}
        config = PacCreatorConfig(**config)
        with self.assertRaises(ValueError) as err:
            config.validate()
        self.assertEqual(str(err.exception), "one proxy has no route")

    def test_get_default_proxy_route(self):
        config = {"proxies": [{"route": "foo"}, {"route": "bar", "tags": ["default"]}]}
        config = PacCreatorConfig(**config)
        self.assertEqual(config.get_default_proxy().route, "bar")

    def test_get_default_proxy_route_with_no_default_proxy(self):
        config = {"proxies": [{"route": "foo"}, {"route": "bar"}]}
        config = PacCreatorConfig(**config)
        self.assertEqual(config.get_default_proxy().route, "foo")

    def test_target_is_string(self):
        config = {"proxies": [{"route": "foo", "targets": [10., "foo"]}]}
        PacCreatorConfig(**config)
