import os
import unittest

from pypac.parser import PACFile

from pypacer import PyPacer
from pypacer.helpers import location
from pypacer.pypacerconfig import PyPacerConfig


class TestPyPacer(unittest.TestCase):

    def setUp(self):
        self.pac_file = open(os.path.join(location, "..", "examples", "pac_unittests.yaml"), "r").read()

    def test_load_config_from_yaml(self):
        p = PyPacer()
        p.load_config_from_yaml(self.pac_file)
        self.assertIsInstance(p.config, PyPacerConfig)
        self.assertEqual(p.config.default, "PROXY_A")

    def test_get_default_proxy_route(self):
        p = PyPacer()
        p.load_config_from_yaml(self.pac_file)
        self.assertEqual(p._get_default_proxy_route(), "PROXY localhost:8080")

    def test_output_default_route(self):
        p = PyPacer()
        p.load_config_from_yaml(self.pac_file)
        pac_file = PACFile(p.output())
        assert pac_file.find_proxy_for_url("foo.bar", "foo.bar") == "PROXY localhost:8080"

    def test_output_foo_example_com(self):
        p = PyPacer()
        p.load_config_from_yaml(self.pac_file)
        pac_file = PACFile(p.output())
        # assert pac_file.find_proxy_for_url("", "foo.example.com") == "PROXY localhost:8081"
