import time
from org.gi.server import utils as u

from org.gi.server.db import db
from org.gi.server.validation.validation_utils import is_a_list, is_a_number
import org.gi.server.service.date_util as date_util

USER_PROJECTION = {
    'first_name': 1,
    'last_name': 1,
    'email': 1,
    'phone_number': 1,
    'notifications': 1
}

DEFAULT_LOCALE = 'he'


def get_petitioner_from_case(case):
    petitioner = {
        'case_title': case.get('title'),
        'user_id': case.get('petitioner_id'),
        'details': _get_user_from_db(case.get('petitioner_id')),
        'tasks': [],
        'volunteers': []
    }
    return petitioner


def get_volunteer_from_case_and_task(case, task):
    volunteer = {
        'case_title': case.get('title'),
        'user_id': task.get('volunteer_id'),
        'details': _get_user_from_db(task.get('volunteer_id')),
        'tasks': [_get_task_details(task)] if task else [],
    }
    return volunteer


def _get_task_details(_task):
    task = {
        'title': _task.get('title'),
        'id': _task.get('id'),
        'volunteer_id': _task.get('volunteer_id'),
        'due_date':  date_util.from_seconds_to_locale_date(_task.get('due_date'), locale=DEFAULT_LOCALE)
    }
    optional_data = ['location', 'destination']
    for data in optional_data:
        if _task.get(data):
            task[data] = _task.get(data)

    return task


def _get_lists_from_cases(cases, upto_due_date):
    petitioner_list = []
    volunteer_list = []
    for case in cases:
        petitioner = get_petitioner_from_case(case)
        for task in case.get('tasks'):
            if task.get('due_date') <= upto_due_date:
                volunteer_list.append(get_volunteer_from_case_and_task(case, task))
                if not is_a_list(petitioner.get('tasks')):
                    petitioner['tasks'] = []
                petitioner['tasks'].append(_get_task_details(task))

        for task in petitioner.get('tasks'):
            petitioner['volunteers'].append(_get_user_from_db(task.get('volunteer_id')))
        petitioner_list.append(petitioner)
    return petitioner_list, volunteer_list


def _get_user_from_db(user_id):
    return db.users.find_one({'_id': u.to_object_id(user_id)}, projection=USER_PROJECTION)


def fetch_users_with_upto_x_hours_until_task(hours_till_task):
    if not (hours_till_task and isinstance(hours_till_task, int)):
        raise Exception('Hours till task must be a legal int')
    curr_time = int(time.time())
    upto_due_date = curr_time + (hours_till_task * 60 * 60)
    return fetch_users_with_tasks_between_x_and_y(curr_time, upto_due_date)


def fetch_users_with_tasks_between_x_and_y(start_time, end_time):
    if not is_a_number(start_time):
        raise Exception('start time task must be a legal int')
    if not is_a_number(end_time):
        raise Exception('end time task must be a legal int')
    filter = {
        'tasks': {
            '$elemMatch': {
                'due_date': {
                    '$gt': start_time,
                    '$lt': end_time
                }
            }
        }
    }
    cases = db.cases.find(filter=filter)
    cases = u.make_list(cases)
    petitioner_list, volunteer_list = _get_lists_from_cases(cases, end_time)
    return petitioner_list, volunteer_list
