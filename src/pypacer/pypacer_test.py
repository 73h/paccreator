import unittest

from pypacer import PyPacer
from pypacer.pypacerconfig import PyPacerConfig


class TestPyPacer(unittest.TestCase):

    def setUp(self):
        self.pac_file = open("/src/examples/pac_unittests.yaml", "r").read()

    def test_load_config_from_yaml(self):
        p = PyPacer()
        p.load_config_from_yaml(self.pac_file)
        self.assertIsInstance(p.config, PyPacerConfig)
        self.assertEqual(p.config.default, "PROXY_A")

    def test_get_default_proxy_route(self):
        p = PyPacer()
        p.load_config_from_yaml(self.pac_file)
        self.assertEqual(p._get_default_proxy_route(), "PROXY localhost:8080")
