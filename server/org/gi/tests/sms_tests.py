import unittest

from org.gi.server.service.send_sms import send_sms


class GISMSTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GISMSTestCase, self).__init__(*args, **kwargs)
        self.test_mode = True

    def test_no_sender(self):
        self.assertRaises(Exception, send_sms, 'sender', None, 'message')

    def test_no_to(self):
        self.assertRaises(Exception, send_sms, None, 'sender', 'message')

    def test_no_message(self):
        self.assertRaises(Exception, send_sms, 'to', 'sender', None)

    @unittest.skip("Skipping... Try sending yourself an SMS ;]")
    def test_send_test_mode_false(self):
        sms_to = '+972527588594'
        sms_from = '+972545450'
        status, resp = send_sms(sms_to, sms_from, 'A msg from GI server')
        self.assertTrue(status)
        self.assertIsNotNone(resp)
