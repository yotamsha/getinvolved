# coding=utf-8
import unittest


from org.gi.server.service.date_util import from_seconds_to_locale_date


class DateUtilTests(unittest.TestCase):
    # positives
    def test_correct_hebrew_date(self):
        time_in_seconds = 1456481327
        self.assertEqual(u"(02/26) יום ו׳ 12:08 אחה״צ", from_seconds_to_locale_date(time_in_seconds))

    def test_correct_english_date(self):
        time_in_seconds = 1456481327
        self.assertEqual(u'(02/26) Fri 12:08 PM', from_seconds_to_locale_date(time_in_seconds, locale='en'))

    def test_correct_english_date(self):
        time_in_seconds = 1456481327
        self.assertEqual(u'(02/26) Fr. 12:08 nachm.', from_seconds_to_locale_date(time_in_seconds, locale='de'))
