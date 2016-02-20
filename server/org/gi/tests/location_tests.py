#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'avishayb'

import unittest

from org.gi.server.service import location as l


class GILocationTestCase(unittest.TestCase):
    def test_location_1(self):
        LAT = 37.4224504
        LNG = -122.0840859
        location = l.get_lat_lng('1600 Amphitheatre Parkway, Mountain View, CA')
        self.assertEqual(location['lat'], LAT)
        self.assertEqual(location['lng'], LNG)

    def test_location_2(self):
        LAT = 32.0666302
        LNG = 34.7942945
        CITY = 'תל-אביב'
        STREET = ' יונה קרמניצקי 6'
        location = l.get_lat_lng(CITY + ' , ' + STREET)
        self.assertEqual(location['lat'], LAT)
        self.assertEqual(location['lng'], LNG)

    def test_location_3(self):
        LAT = 32.0753543
        LNG = 34.77528300000001
        location = l.get_lat_lng('Dizengoff St 50, Tel Aviv-Yafo, 64332')
        self.assertEqual(location['lat'], LAT)
        self.assertEqual(location['lng'], LNG)

    def test_location_4(self):
        LAT = 32.0666302
        LNG = 34.7942945
        CITY = 'תל-אביב'
        STREET = ' יונה קרמניצקי'
        address = {'city': CITY, 'country': 'ישראל', 'street_name': STREET, 'street_number': '6'}
        location = l.get_lat_lng(address)
        self.assertEqual(location['lat'], LAT)
        self.assertEqual(location['lng'], LNG)

    def test_location_5(self):
        STREET = ' יונה קרמניצקי'
        address = {'country': 'ישראל', 'street_name': STREET, 'street_number': '6'}
        self.assertRaises(Exception, l.get_lat_lng, address)

    def test_location_6(self):
        self.assertRaises(Exception, l.get_lat_lng, '??????????')

    def test_location_7(self):
        self.assertRaises(Exception, l.get_lat_lng, None)

    def test_location_8(self):
        self.assertRaises(Exception, l.get_lat_lng, [1])

    def test_location_reverse_1(self):
        LAT = 32.0666302
        LNG = 34.7942945
        CITY = u' תל אביב יפו'
        STREET = u'יונה קרמנצקי 6'
        CONTRY = u' ישראל'
        address = l.get_address(LAT, LNG)
        self.assertEqual(address.get('street'), STREET)
        self.assertEqual(address.get('city'), CITY)
        self.assertEqual(address.get('country'), CONTRY)

    def test_location_reverse_2(self):
        self.assertRaises(Exception, l.get_address, '', '')

    def test_location_reverse_3(self):
        self.assertRaises(Exception, l.get_address, '34.678', '33.789')

