# coding=utf-8
import logging

from org.gi.server.service.send_email import send_email
from org.gi.server.service.send_sms import send_sms
from org.gi.server.validation.validations import validate_phone_number

GI_PHONE_NUMBER = '054-443-3218'  # Note this is Dana Cohen's personal phone number
GI_EMAIL_ADDRESS = "info@getinvolved.org.il"


class MessageSender:
    def __init__(self):
        pass

    def send_sms_to(self, recipient, sms, sender=GI_PHONE_NUMBER):
        if recipient.get('phone_number'):
            faults = []
            validate_phone_number(recipient.get('phone_number'), faults)
            if faults:
                self._error(faults)
                return
        else:
            self._error('Cannot send SMS to user with no phonenumber: {}'.format(recipient))
            return
        if not (sms and len(sms) > 0 and isinstance(sms, basestring)):
            self._error('Cannot send SMS with no message')
            return
        try:
            recipient_phone_number = recipient.get('phone_number').get('number')
            success, response = send_sms(recipient_phone_number, sender, sms)
        except Exception:
            success = False
        if not success:
            reason = response.content if response.content else ""
            self._error('Failed sending SMS to following user: {},\n Reason: {}'.format(recipient, reason))

    def send_email_to(self, recipient, subject, message, sender=GI_EMAIL_ADDRESS):
        if not recipient.get('email'):
            self._error('Cannot send EMAIL to user: {}'.format(recipient))
            return
        success, resp_id = send_email(recipient.get('email'), subject, message, sender)
        if not success:
            self._error('Failed sending EMAIL to following user: {},\n Response_ID: {}'.format(recipient, resp_id))

    def patch(self):
        self.send_email_to = self.write_email_to_log
        self.send_sms_to = self.write_sms_to_log

    @staticmethod
    def write_email_to_log(recipient, subject, message, sender=GI_EMAIL_ADDRESS):
        logging.info("Sending email...")
        logging.info(" From: {}".format(sender))
        logging.info(" To: {}".format(recipient))
        logging.info(" Subject: %r" % subject)
        logging.info(" Body: %r" % message)

    @staticmethod
    def write_sms_to_log(recipient, sms, sender=GI_PHONE_NUMBER):
        logging.info("Sending sms...")
        logging.info(" From: {}".format(sender))
        logging.info(" To: {}".format(recipient))
        logging.info(" Body: %r" % sms)

    def _error(self, msg):
        self._error(msg)
