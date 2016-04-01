# - *- coding: utf- 8 - *-

import unittest

from org.gi.server.validation import validations
from org.gi.server.validation import validation_utils


class ValidationsTest(unittest.TestCase):
    def test_is_user_id(self):
        self.assertTrue(validations.is_user_id('54f0e5aa313f5d824680d6c9'))
        self.assertFalse(validations.is_user_id('54f0e5aa313f5d824680d'))

    def test_len_range_unicode_support(self):
        description = u'אם חד הורית עם מוגבלות פיזית זקוקה לעזרה בפריקת ארגזים לאחר מעבר דירה'
        self.assertTrue(validation_utils.validate_len_in_range('task', 'description', description))
