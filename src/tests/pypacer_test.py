import os
import pathlib
import unittest

from pypac.parser import PACFile

from pypacer import PyPacer
from pypacer.pypacerconfig import PyPacerConfig

location = pathlib.Path(__file__).parent.resolve()


class TestPyPacer(unittest.TestCase):

    def setUp(self):
        self.pac_file = open(os.path.join(location, "..", "examples", "unittests.yaml"), "r").read()

    def test_load_config_from_yaml(self):
        p = PyPacer()
        p.load_from_yaml(self.pac_file)
        self.assertIsInstance(p.config, PyPacerConfig)
        self.assertTrue(p.config.proxies['proxy_default'].default)
        output = p.output()
        open(os.path.join(location, "..", "examples", "unittests.pac"), "w").write(output)

    def test_output(self):
        p = PyPacer()
        p.load_from_yaml(self.pac_file)
        pac_file = PACFile(p.output())
        self.assertEqual(pac_file.find_proxy_for_url("", "foo.bar"), "PROXY default.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "foo.example.com"), "PROXY domain-overlaps.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "bar.example.com"), "PROXY mixed.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "example.org"), "PROXY netmask.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "ipv4only.arpa"), "PROXY ip.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "10.11.12.13"), "PROXY string.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "192.168.102.123"), "PROXY string.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "127.0.0.1"), "PROXY ip.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "intranet"), "PROXY plain-hostname.example.com")
        self.assertEqual(pac_file.find_proxy_for_url("", "x.y.z"), "PROXY default.example.com")
