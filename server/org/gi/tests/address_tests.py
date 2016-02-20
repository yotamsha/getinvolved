__author__ = 'avishayb'
import unittest

from misc import _load
from org.gi.server.validation import location_validator as v


class GIAddressValidationTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIAddressValidationTestCase, self).__init__(*args, **kwargs)
        self.config_folder = 'address'

    def test_address(self):
        addr = _load('empty_address.json', self.config_folder)
        faults = []
        v.validate_address(addr, faults)
        self.assertEqual(len(faults), 1)

    def test_half_address(self):
        addr = _load('half_empty_address.json', self.config_folder)
        faults = []
        v.validate_address(addr, faults)
        self.assertEqual(len(faults), 1)

    def test_wrong_country(self):
        addr = _load('wrong_country_address.json', self.config_folder)
        faults = []
        v.validate_address(addr, faults)
        self.assertEqual(len(faults), 1)

    def test_address_ok(self):
        addr = _load('address.json', self.config_folder)
        faults = []
        v.validate_address(addr, faults)
        self.assertEqual(len(faults), 0)

