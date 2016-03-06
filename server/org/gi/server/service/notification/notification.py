# coding=utf-8
import time
import logging

from org.gi.server.service.notification.fetch_users_to_notify import fetch_users_with_tasks_between_x_and_y
from org.gi.server.service.send_email import send_email
from org.gi.server.service.send_sms import send_sms
from org.gi.server.service.templates.templates import load_and_merge
from org.gi.server.validation.validations import validate_phone_number

SECONDS_IN_HOUR = 60 * 60

current_time = -1
last_update_time = -1
NOTIFICATION_WINDOW_IN_SECONDS = SECONDS_IN_HOUR
HEBREW = 'he'
GI_PHONE_NUMBER = '054-443-3218'  # Note this is Dana Cohen's personal phone number
GI_EMAIL_ADDRESS = "info@getinvolved.org.il"
FIRST_REMINDER_HOURS = 24
SECOND_REMINDER_HOURS = 3
FIRST_REMINDER_TEMPLATE = 'first_reminder'
SECOND_REMINDER_TEMPLATE = 'second_reminder'
VOLUNTEER = 'volunteer'
PETITIONER = 'petitioner'
FIRST_REMINDER_SUBJECT = u"GetInvolved - התראה"
SECOND_REMINDER_SUBJECT = u"GetInvolved - התראה"


def send_sms_to(recipient, sms, sender=GI_PHONE_NUMBER):
    if recipient.get('phone_number'):
        faults = []
        validate_phone_number(recipient.get('phone_number'), faults)
        if faults:
            logging.error(faults)
            return
    else:
        logging.error('Cannot send SMS to user with no phonenumber: {}'.format(recipient))
        return
    if not (sms and len(sms) > 0 and isinstance(sms, basestring)):
        logging.error('Cannot send SMS with no message')
        return
    try:
        recipient_phone_number = recipient.get('phone_number').get('number')
        success, response = send_sms(recipient_phone_number, sender, sms)
    except Exception:
        success = False
    if not success:
        reason = response.content if response.content else ""
        logging.error('Failed sending SMS to following user: {},\n Reason: {}'.format(recipient, reason))


def send_email_to(recipient, subject, message, sender=GI_EMAIL_ADDRESS):
    if not recipient.get('email'):
        logging.error('Cannot send EMAIL to user: {}'.format(recipient))
        return
    success, resp_id = send_email(recipient.get('email'), subject, message, sender)
    if not success:
        logging.error('Failed sending EMAIL to following user: {},\n Response_ID: {}'.format(recipient, resp_id))


def add_gi_email_and_phone_to_data(user_data):
    user_data['gi_email'] = GI_EMAIL_ADDRESS
    user_data['gi_phone'] = GI_PHONE_NUMBER


def _send_email_and_sms(user_data, subject, template, user_type, sms=True, email=True, lang=HEBREW):
    add_gi_email_and_phone_to_data(user_data)
    notification_settings = NotificationSettings(user_data.get('details').get('notifications'))
    if notification_settings.sms_enabled and sms:
        sms_notfication = load_and_merge('/{}/sms/{}'.format(user_type, template), user_data, lang)
        send_sms_to(user_data.get('details'), sms_notfication)
    if notification_settings.email_enabled and email:
        email_notification = load_and_merge('/{}/email/{}'.format(user_type, template), user_data, lang)
        send_email_to(user_data.get('details'), subject, email_notification)


def _do_first_notifications():
    petitioner_list, volunteer_list = _get_users_with_tasks_in_x_hours(FIRST_REMINDER_HOURS)
    for petitioner in petitioner_list:
        _send_email_and_sms(petitioner, FIRST_REMINDER_SUBJECT, 'first_reminder', 'petitioner')
    for volunteer in volunteer_list:
        _send_email_and_sms(volunteer, FIRST_REMINDER_SUBJECT, 'first_reminder', 'volunteer')


def _do_second_notifications():
    petitioner_list, volunteer_list = _get_users_with_tasks_in_x_hours(SECOND_REMINDER_HOURS)
    for petitioner in petitioner_list:
        _send_email_and_sms(petitioner, SECOND_REMINDER_SUBJECT, 'second_reminder', 'petitioner')
    for volunteer in volunteer_list:
        _send_email_and_sms(volunteer, SECOND_REMINDER_SUBJECT, 'second_reminder', 'volunteer')


def notify():
    global current_time
    global last_update_time
    current_time = _get_current_time()
    _do_first_notifications()
    _do_second_notifications()
    last_update_time = current_time


def _get_current_time():
    return int(time.time())


def _time_lapse():
    if last_update_time < 0:
        return 0
    return current_time - last_update_time


def _get_users_with_tasks_in_x_hours(hours):
    return fetch_users_with_tasks_between_x_and_y(
            current_time + (hours * SECONDS_IN_HOUR),
            current_time + (hours * SECONDS_IN_HOUR) + _time_lapse())


DEFAULT_SMS_NOTIFICATIONS = False
DEFAULT_EMAIL_NOTIFICATIONS = True


class NotificationSettings(object):
    def __init__(self, notification_dict):
        if notification_dict:
            self.sms_enabled = notification_dict.get('sms') if 'sms' in notification_dict \
                else DEFAULT_SMS_NOTIFICATIONS
            self.email_enabled = notification_dict.get('email') if 'email' in notification_dict \
                else DEFAULT_EMAIL_NOTIFICATIONS
        else:
            self.sms_enabled = DEFAULT_SMS_NOTIFICATIONS
            self.email_enabled = DEFAULT_EMAIL_NOTIFICATIONS
