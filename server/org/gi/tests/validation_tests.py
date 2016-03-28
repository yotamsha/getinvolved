import unittest

from org.gi.server.validation import validations


class ValidationsTest(unittest.TestCase):
    def test_is_user_id(self):
        self.assertTrue(validations.is_user_id('54f0e5aa313f5d824680d6c9'))
        self.assertFalse(validations.is_user_id('54f0e5aa313f5d824680d'))
