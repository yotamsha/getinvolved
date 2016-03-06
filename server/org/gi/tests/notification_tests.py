import unittest

import requests
import time
from mock import Mock, call
import org.gi.server.service.notification.notification as notification
from org.gi.tests.misc import _load, SERVER_URL_API, ACCESS_TOKEN_AUTH, MONGO, _push_to_db, _remove_from_db


class GINotificationTests(unittest.TestCase):
    def setUp(self):
        self.real_first_notifications = notification._do_first_notifications
        self.real_second_notifications = notification._do_second_notifications
        self.real_fetch_users = notification.fetch_users_with_tasks_between_x_and_y
        self.real_logging_error = notification.logging.error
        self.real_send_email_or_sms = notification._send_email_and_sms
        self.real_send_sms_to = notification.send_sms_to
        self.real_send_email_to = notification.send_email_to
        self.real_time_time = notification.time.time
        _remove_from_db(MONGO, 'users')
        _remove_from_db(MONGO, 'cases')

    def tearDown(self):
        notification._do_first_notifications = self.real_first_notifications
        notification._do_second_notifications = self.real_second_notifications
        notification.fetch_users_with_tasks_between_x_and_y = self.real_fetch_users
        notification.logging.error = self.real_logging_error
        notification._send_email_and_sms = self.real_send_email_or_sms
        notification.send_sms_to = self.real_send_sms_to
        notification.send_email_to = self.real_send_email_to
        notification.time.time = self.real_time_time

    def test_methods_called(self):
        curr_time = 1000
        notification._do_first_notifications = Mock()
        notification._do_second_notifications = Mock()
        notification._get_current_time = Mock(return_value=curr_time)

        notification.notify()
        notification._do_first_notifications.assert_called_with()
        notification._do_second_notifications.assert_called_with()
        self.assertEqual(curr_time, notification.last_update_time)

    def test_fetch_users_between(self):
        hours = 3
        curr_time = 150
        diff = 50
        notification.fetch_users_with_tasks_between_x_and_y = Mock()
        notification.current_time = curr_time
        notification.last_update_time = curr_time - diff

        start_time = curr_time + (hours * notification.SECONDS_IN_HOUR)
        end_time = start_time + diff

        notification._get_users_with_tasks_in_x_hours(hours)
        notification.fetch_users_with_tasks_between_x_and_y.assert_called_with(start_time, end_time)

    def test_first_notifications_send_emails_and_sms(self):
        petitioner_list = ['a', 'b']
        volunteer_list = ['c', 'd']
        notification._get_users_with_tasks_in_x_hours = Mock(return_value=(petitioner_list, volunteer_list))
        notification._send_email_and_sms = Mock()
        notification._do_first_notifications()
        calls = [
            call('a', notification.FIRST_REMINDER_SUBJECT, notification.FIRST_REMINDER_TEMPLATE, notification.PETITIONER),
            call('b', notification.FIRST_REMINDER_SUBJECT, notification.FIRST_REMINDER_TEMPLATE, notification.PETITIONER),
            call('c', notification.FIRST_REMINDER_SUBJECT, notification.FIRST_REMINDER_TEMPLATE, notification.VOLUNTEER),
            call('d', notification.FIRST_REMINDER_SUBJECT, notification.FIRST_REMINDER_TEMPLATE, notification.VOLUNTEER),
        ]
        notification._send_email_and_sms.assert_has_calls(calls, any_order=False)

    def test_second_notifications_send_emails_and_sms(self):
        petitioner_list = ['a', 'b']
        volunteer_list = ['c', 'd']
        notification._get_users_with_tasks_in_x_hours = Mock(return_value=(petitioner_list, volunteer_list))
        notification._send_email_and_sms = Mock()
        notification._do_second_notifications()
        calls = [
            call('a', notification.SECOND_REMINDER_SUBJECT, notification.SECOND_REMINDER_TEMPLATE, notification.PETITIONER),
            call('b', notification.SECOND_REMINDER_SUBJECT, notification.SECOND_REMINDER_TEMPLATE, notification.PETITIONER),
            call('c', notification.SECOND_REMINDER_SUBJECT, notification.SECOND_REMINDER_TEMPLATE, notification.VOLUNTEER),
            call('d', notification.SECOND_REMINDER_SUBJECT, notification.SECOND_REMINDER_TEMPLATE, notification.VOLUNTEER),
        ]
        notification._send_email_and_sms.assert_has_calls(calls, any_order=False)

    def test_send_email_and_sms(self):
        all_data = _load('real_world_volunteer.json', 'template')
        user_data = all_data['data']
        template = 'first_reminder'
        user_type = 'volunteer'
        notification.send_sms_to = Mock()
        notification.send_email_to = Mock()

        user_data['details']['notifications'] = {
            'sms': False,
            'email': False
        }
        notification._send_email_and_sms(user_data, 'subject', template, user_type)
        notification.send_sms_to.assert_not_called()
        notification.send_email_to.assert_not_called()
        user_data['details']['notifications'] = {
            'sms': True,
            'email': True
        }
        notification._send_email_and_sms(user_data, 'subject', template, user_type)
        self.assertTrue(notification.send_sms_to.called)
        self.assertTrue(notification.send_email_to.called)

    def test_last_update_time_saved(self):
        notification._do_first_notifications = Mock()
        notification._do_second_notifications = Mock()
        notification.time.time = Mock(return_value=100)
        notification.notify()
        self.assertEqual(100, notification.last_update_time)

    # negatives
    def test_no_phone_number(self):
        notification.logging.error = Mock()
        msg = 'the msg'
        recipient = {'name': 'nada'}
        notification.send_sms_to(recipient, msg)
        notification.logging.error.assert_called_with("Cannot send SMS to user with no phonenumber: {'name': 'nada'}")
        recipient = {'name': 'nada', 'phone_number': {'number': '030303', 'country_code': 'IL'}}
        notification.send_sms_to(recipient, msg)
        notification.logging.error.assert_called_with(['The phone number 030303 (country IL) is invalid.'])

    def test_no_msg(self):
        notification.logging.error = Mock()
        recipient = {'name': 'nada', 'phone_number': {'number': '0543030303'}}
        notification.send_sms_to(recipient, None)
        notification.logging.error.assert_called_with(["phone_number must contain the field 'country_code'"])

    @unittest.skip("Skipping... This one really sends notifications")
    def test_real_notify(self):
        # Insert 2 users and keep ids
        # Add case with tasks assigned to created users
        users = _load('users.json', "notification")['users']
        user_ids = []
        users[0]['email'] = 'barwachtel@gmail.com'  # petitioner first reminder
        users[1]['phone_number']['number'] = '+972527588594'  # volunteer first reminder
        for user in users:
            r = requests.post('%s/users' % SERVER_URL_API, auth=ACCESS_TOKEN_AUTH, json=user)
            user_ids.append(r.json().get('id'))
        case = _load('case.json', "notification")
        case['petitioner_id'] = user_ids[0]
        tasks = case.get('tasks')
        tasks[0]['due_date'] = int(time.time()) + int(notification.SECONDS_IN_HOUR * 24) + 300
        tasks[0]['volunteer_id'] = user_ids[1]
        _push_to_db(MONGO, 'cases', [case])
        notification.last_update_time = int(time.time()) - 1000
        notification.notify()
