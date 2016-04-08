import unittest

import requests
import time
from mock import Mock, call

from org.gi.server.service.notification import notification
from org.gi.server.validation.case_state_machine import CASE_PENDING_APPROVAL, CASE_PENDING_INVOLVEMENT, CASE_ASSIGNED, \
    CASE_COMPLETED
from org.gi.server.validation.task.task_state_machine import TASK_ASSIGNED, TASK_COMPLETED, TASK_PENDING
from org.gi.tests.misc import _load, SERVER_URL_API, ACCESS_TOKEN_AUTH, MONGO, _push_to_db, _remove_from_db


class GINotificationTests(unittest.TestCase):
    def setUp(self):
        notification.message_sender = Mock()
        self.real_first_notifications = notification._do_first_notifications
        self.real_second_notifications = notification._do_second_notifications
        self.real_fetch_users = notification.fetch_users_with_tasks_between_x_and_y
        self.real_send_email_or_sms = notification._send_email_and_sms
        self.real_time_time = notification.time.time

    def tearDown(self):
        notification._do_first_notifications = self.real_first_notifications
        notification._do_second_notifications = self.real_second_notifications
        notification.fetch_users_with_tasks_between_x_and_y = self.real_fetch_users
        notification._send_email_and_sms = self.real_send_email_or_sms
        notification.time.time = self.real_time_time
        _remove_from_db(MONGO, 'users')
        _remove_from_db(MONGO, 'cases')

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

        user_data['details']['notifications'] = {
            'sms': False,
            'email': False
        }
        notification._send_email_and_sms(user_data, 'subject', template, user_type)
        notification.message_sender.send_email_to.assert_not_called()
        notification.message_sender.send_sms_to.assert_not_called()
        user_data['details']['notifications'] = {
            'sms': True,
            'email': True
        }
        notification._send_email_and_sms(user_data, 'subject', template, user_type)
        self.assertTrue(notification.message_sender.send_sms_to.called)
        self.assertTrue(notification.message_sender.send_email_to.called)

    def test_last_update_time_saved(self):
        notification._do_first_notifications = Mock()
        notification._do_second_notifications = Mock()
        notification.time.time = Mock(return_value=100)
        notification.notify()
        self.assertEqual(100, notification.last_update_time)

    def test_send_case_approval(self):
        old_case = {'state': CASE_PENDING_APPROVAL}
        db_case = {'state': CASE_PENDING_INVOLVEMENT, 'tasks': []}
        notification._send_case_approval_email = Mock()
        notification.send_user_notifications(db_case, old_case)
        notification._send_case_approval_email.assert_called_once()

    def test_send_petitioner_match(self):
        old_case = {'state': CASE_PENDING_INVOLVEMENT}
        db_case = {'state': CASE_ASSIGNED, 'tasks': []}
        notification._send_petitioner_match_email = Mock()
        notification.send_user_notifications(db_case, old_case)
        notification._send_petitioner_match_email.assert_called_once()

    def test_send_volunteers_feedback(self):
        old_case = {'state': CASE_ASSIGNED}
        db_case = {'state': CASE_COMPLETED, 'tasks': []}
        notification._send_volunteers_feedback_email = Mock()
        notification.send_user_notifications(db_case, old_case)
        notification._send_volunteers_feedback_email.assert_called_once()

    def test_send_volunteer_register_to_case(self):
        old_case = {'state': CASE_ASSIGNED, 'tasks': [{'id': 0, 'state': TASK_PENDING}]}
        db_case = {'state': CASE_ASSIGNED, 'tasks': [{'id': 0, 'state': TASK_ASSIGNED}]}
        notification._send_volunteer_register_to_case_email = Mock()
        notification.send_user_notifications(db_case, old_case)
        notification._send_volunteer_register_to_case_email.assert_called_once()

    # negatives
    @unittest.skip("Skipping... This one really sends notifications")
    def test_send_out_live_emails(self):
        users = _load('online_notify_users.json', 'notification')
        nina = users[0]
        viktor = users[1]
        # Place your mail to recieve notifications, CANT BE THE SAME MAIL!
        nina['email'] = "barwachtel@gmail.com"
        viktor['email'] = "bar@my6sense.com"
        nina = requests.post('%s/users' % SERVER_URL_API, auth=ACCESS_TOKEN_AUTH, json=nina).json()
        viktor = requests.post('%s/users' % SERVER_URL_API, auth=ACCESS_TOKEN_AUTH, json=viktor).json()
        case = _load('online_notify_case.json', 'notification')
        case['petitioner_id'] = nina['id']
        case['tasks'][0]['due_date'] = self._replace_due_date()
        case = requests.post('%s/cases' % SERVER_URL_API, auth=ACCESS_TOKEN_AUTH, json=case).json()
        task = case.get('tasks')[0]
        task['volunteer_id'] = viktor['id']
        # sends petitioner case approval mail (Illegal transition but what the heck)
        case = requests.put('%s/cases/%s' % (SERVER_URL_API, case['id']), auth=ACCESS_TOKEN_AUTH, json=case).json()
        case['tasks'][0]['state'] = TASK_ASSIGNED
        # sends petitioner match mail
        # sends volunteer register to case mail
        case = requests.put('%s/cases/%s' % (SERVER_URL_API, case['id']), auth=ACCESS_TOKEN_AUTH, json=case).json()
        case['tasks'][0]['state'] = TASK_COMPLETED
        case['tasks'][0]['duration'] = 1000
        # sends volunteer feedback mail
        case = requests.put('%s/cases/%s' % (SERVER_URL_API, case['id']), auth=ACCESS_TOKEN_AUTH, json=case).json()

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
        tasks[0]['due_date'] = self._replace_due_date()
        tasks[0]['volunteer_id'] = user_ids[1]
        _push_to_db(MONGO, 'cases', [case])
        notification.last_update_time = int(time.time()) - 1000
        notification.notify()

    def _replace_due_date(self):
        return int(time.time()) + int(notification.SECONDS_IN_HOUR * 24) + 300
