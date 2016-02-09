__author__ = 'avishayb'
import unittest

from org.gi.server.services import url_shortener as shortener


class GIShortURLTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIShortURLTestCase, self).__init__(*args, **kwargs)

    def test_get_short_url(self):
        status, short_url = shortener.get_short_url('http://www.shvoong.co.il')
        self.assertTrue(status)
        self.assertEqual(short_url,'http://bit.ly/1RkShZd')

    def test_get_short_url_dummy_data(self):
        status, short_url = shortener.get_short_url('not a url...')
        self.assertFalse(status)

    def test_get_short_url_using_dict(self):
        self.assertRaises(Exception, shortener.get_short_url, {})

    def test_get_short_url_using_none(self):
        self.assertRaises(Exception, shortener.get_short_url, None)

