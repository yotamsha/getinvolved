# - *- coding: utf- 8 - *-

import unittest

from org.gi.server.validation import validations
from org.gi.server.validation import validation_utils


class ValidationsTest(unittest.TestCase):
    def test_is_user_id(self):
        self.assertTrue(validations.is_user_id('54f0e5aa313f5d824680d6c9'))
        self.assertFalse(validations.is_user_id('54f0e5aa313f5d824680d'))

    def test_len_range_unicode_support(self):
        description_heb = u'אם חד הורית עם מוגבלות פיזית זקוקה לעזרה בפריקת ארגזים לאחר מעבר דירה'
        self.assertTrue(validation_utils.validate_len_in_range('task', 'description', description_heb))
        description_spa = u'Érase una vez que había una mamá cerda que tenía tres cerditos'
        self.assertTrue(validation_utils.validate_len_in_range('task', 'description', description_spa))


    def test_entity_not_found(self):
        self.assertRaises(ValueError, validation_utils.validate_len_in_range, '__u_cant_find_me', '__', '')

    def test_field_not_found(self):
        self.assertRaises(ValueError, validation_utils.validate_len_in_range, 'user', 'no_way..', '')

    def test_value_is_none(self):
        self.assertRaises(ValueError, validation_utils.validate_len_in_range, 'user', 'description', None)

    def test_value_is_dict(self):
        self.assertRaises(ValueError, validation_utils.validate_len_in_range, 'user', 'description', {})

    def test_len_range_short(self):
        self.assertFalse(validation_utils.validate_len_in_range('task', 'description', 'short'))

    def test_len_range_long(self):
        self.assertFalse(validation_utils.validate_len_in_range('task', 'description', 'long' * 100))

    def test_not_a_mobile_number(self):
        faults = []
        validations.validate_phone_number({'number': '036497314','country_code': 'IL'},faults)
        self.assertEqual(len(faults),1)

    def test_is_a_mobile_number(self):
        faults = []
        validations.validate_phone_number({'number': '0544280114','country_code': 'IL'},faults)
        self.assertEqual(len(faults),0)


