# coding=utf-8
import os
import time

from org.gi.server.model.Task import Task
from org.gi.server.service.notification.fetch_users_to_notify import fetch_users_with_tasks_between_x_and_y, \
    get_petitioner_from_case, get_volunteer_from_case_and_task
from org.gi.server.service.notification.message_sender import MessageSender
from org.gi.server.service.templates.templates import load_and_merge
from org.gi.server.validation.case_state_machine import CASE_PENDING_APPROVAL, CASE_PENDING_INVOLVEMENT, \
    CASE_PARTIALLY_ASSIGNED, CASE_ASSIGNED, CASE_PARTIALLY_COMPLETED, CASE_COMPLETED
from org.gi.server.validation.task.task_state_machine import TASK_PENDING_USER_APPROVAL, TASK_ASSIGNMENT_IN_PROCESS, \
    TASK_PENDING, TASK_ASSIGNED

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
CASE_APPROVAL_SUBJECT = u"GetInvolved - אישור העלת מקרה"
CASE_VOLUNTEER_MATCH_SUBJECT = u"GetInvolved - נמצא מתנדב למקרה"
VOLUNTEER_FEEDBACK_SUBJECT = u"GetInvolved - משוב מתנדבים"
VOLUNTEER_REGISTER_TO_CASE = u"GetInvolved - נרשמת בהצלחה למקרה"

# Methods are patched at runtime
global message_sender
message_sender = MessageSender()
if os.environ['__MODE'] != 'production':
    message_sender.patch()


def send_user_notifications(db_case, old_case):
    if old_case.get('state') in {CASE_PENDING_APPROVAL}:
        if db_case.get('state') in {CASE_PENDING_INVOLVEMENT}:
            _send_case_approval_email(old_case)

    if old_case.get('state') in {CASE_PENDING_INVOLVEMENT, CASE_PARTIALLY_ASSIGNED}:
        if db_case.get('state') in {CASE_ASSIGNED}:
            _send_petitioner_match_email(old_case)

    if old_case.get('state') in {CASE_ASSIGNED, CASE_PARTIALLY_COMPLETED}:
        if db_case.get('state') in {CASE_COMPLETED}:
            _send_volunteers_feedback_email(old_case)

    _send_emails_to_volunteers_register_to_case(db_case, old_case)


def add_gi_email_and_phone_to_data(user_data):
    user_data['gi_email'] = GI_EMAIL_ADDRESS
    user_data['gi_phone'] = GI_PHONE_NUMBER


def _send_email_and_sms(user_data, subject, template, user_type, sms=True, email=True, lang=HEBREW):
    add_gi_email_and_phone_to_data(user_data)
    notification_settings = NotificationSettings(user_data.get('details').get('notifications'))
    if notification_settings.sms_enabled and sms:
        sms_notfication = load_and_merge('/{}/sms/{}'.format(user_type, template), user_data, lang)
        message_sender.send_sms_to(user_data.get('details'), sms_notfication)
    if notification_settings.email_enabled and email:
        email_notification = load_and_merge('/{}/email/{}'.format(user_type, template), user_data, lang)
        message_sender.send_email_to(user_data.get('details'), subject, email_notification)


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


def _send_case_approval_email(db_case):
    petitioner = get_petitioner_from_case(db_case)
    _send_email_and_sms(petitioner, CASE_APPROVAL_SUBJECT, 'case_approval', 'petitioner', sms=False)


def _send_petitioner_match_email(db_case):
    petitioner = get_petitioner_from_case(db_case)
    _send_email_and_sms(petitioner, CASE_VOLUNTEER_MATCH_SUBJECT, 'match', 'petitioner', sms=False)


def _send_volunteers_feedback_email(db_case):
    for task in db_case.get('tasks'):
        volunteer = get_volunteer_from_case_and_task(db_case, task)
        _send_email_and_sms(volunteer, VOLUNTEER_FEEDBACK_SUBJECT, 'feedback', 'volunteer', sms=False)


def _send_volunteer_register_to_case_email(db_case, task):
    petitioner = get_volunteer_from_case_and_task(db_case, task)
    _send_email_and_sms(petitioner, VOLUNTEER_REGISTER_TO_CASE, 'register_to_case', 'volunteer', sms=False)


def _send_emails_to_volunteers_register_to_case(db_case, old_case):
    for task in db_case.get('tasks'):
        if 'id' in task:
            old_task = Task.get_task_by_id(task.get('id'), old_case.get('tasks'))
            if old_task.get('state') in {TASK_PENDING, TASK_ASSIGNMENT_IN_PROCESS, TASK_PENDING_USER_APPROVAL}:
                if task.get('state') in {TASK_ASSIGNED}:
                    _send_volunteer_register_to_case_email(db_case, task)


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
