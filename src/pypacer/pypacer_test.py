import os
import unittest

from pypac.parser import PACFile

from pypacer import PyPacer
from pypacer.helpers import location
from pypacer.pypacerconfig import PyPacerConfig


class TestPyPacer(unittest.TestCase):

    def setUp(self):
        self.pac_file = open(os.path.join(location, "..", "examples", "unittests.yaml"), "r").read()

    def test_load_config_from_yaml(self):
        p = PyPacer()
        p.load_config_from_yaml(self.pac_file)
        output = p.output()
        open(os.path.join(location, "..", "examples", "unittests.pac"), "w").write(output)
        self.assertIsInstance(p.config, PyPacerConfig)
        self.assertEqual(p.config.default, "PROXY_DEFAULT")

    def test_get_default_proxy_route(self):
        p = PyPacer()
        p.load_config_from_yaml(self.pac_file)
        self.assertEqual(p._get_default_proxy_route(), "PROXY default.example.com")

    def test_output(self):
        p = PyPacer()
        p.load_config_from_yaml(self.pac_file)
        pac_file = PACFile(p.output())
        self.assertEqual(pac_file.find_proxy_for_url("", "foo.bar"), "PROXY default.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "foo.example.com"), "PROXY company.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "example.org"), "PROXY netmask.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "ipv4only.arpa"), "PROXY netmask.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "127.0.0.1"), "PROXY netmask.example.com")
