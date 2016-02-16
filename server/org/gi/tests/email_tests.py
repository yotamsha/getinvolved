__author__ = 'avishayb'
import unittest

from org.gi.server.service import send_email as e


class GIEmailTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIEmailTestCase, self).__init__(*args, **kwargs)
        self.sender = 'startgetinvolved@gmail.com'
        self.to = 'startgetinvolved@gmail.com'
        self.message = 'Test body'
        self.subject = 'A Test message from GI Server'
        self.test_mode = True

    def test_send_test_mode_true(self):
        status, other = e.send_email(self.to, self.subject, self.message, self.sender, test_mode=self.test_mode)
        self.assertTrue(status)
        self.assertIsNotNone(other)

    @unittest.skip("Skipping... This one really sends an email and we do not want to spam")
    def test_send_test_mode_false(self):
        status, other = e.send_email(self.to, self.subject, self.message, self.sender, test_mode=False)
        self.assertTrue(status)
        self.assertIsNotNone(other)
