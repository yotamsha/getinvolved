import unittest

from mock import Mock

from org.gi.server.service.notification.message_sender import MessageSender


class GIMessageSenderTests(unittest.TestCase):
    def test_no_phone_number(self):
        message_sender = MessageSender()
        message_sender._error = Mock()
        msg = 'the msg'
        recipient = {'name': 'nada'}
        message_sender.send_sms_to(recipient, msg)
        message_sender._error.assert_called_with("Cannot send SMS to user with no phonenumber: {'name': 'nada'}")
        recipient = {'name': 'nada', 'phone_number': {'number': '030303', 'country_code': 'IL'}}
        message_sender.send_sms_to(recipient, msg)
        message_sender._error.assert_called_with(['The phone number 030303 (country IL) is invalid.'])
        
    def test_no_msg(self):
        message_sender = MessageSender()
        message_sender._error = Mock()
        recipient = {'name': 'nada', 'phone_number': {'number': '0543030303'}}
        message_sender.send_sms_to(recipient, None)
        message_sender._error.assert_called_with(["phone_number must contain the field 'country_code'"])
        
        
        
        