import time
from org.gi.server import utils as u

from org.gi.server.db import db
from org.gi.server.validation.validation_utils import is_a_list

USER_PROJECTION = {
    'first_name': 1,
    'last_name': 1,
    'email': 1,
    'phone_number': 1,
    'notifications': 1
}


def __get_petitioner_from_case(case):
    petitioner = {
        'case_title': case.get('title'),
        'user_id': case.get('petitioner_id'),
        'details': db.users.find_one({'_id': u.to_object_id(case.get('petitioner_id'))}, projection=USER_PROJECTION),
        'tasks': []
    }
    return petitioner


def __get_volunteer_from_case_and_task(case, task):
    volunteer = {
        'case_title': case.get('title'),
        'user_id': task.get('volunteer_id'),
        'details': db.users.find_one({'_id': u.to_object_id(task.get('volunteer_id'))}, projection=USER_PROJECTION),
        'tasks': [__get_task_name_and_id(task)]
    }
    return volunteer


def __get_task_name_and_id(_task):
    task = {
        'task_title': _task.get('title'),
        'id': _task.get('id')
    }
    return task


def __get_lists_from_cases(cases, upto_due_date):
    petitioner_list = []
    volunteer_list = []
    for case in cases:
        petitioner = __get_petitioner_from_case(case)
        for task in case.get('tasks'):
            if task.get('due_date') <= upto_due_date:
                volunteer_list.append(__get_volunteer_from_case_and_task(case, task))
                if not is_a_list(petitioner.get('tasks')):
                    petitioner['tasks'] = []
                petitioner['tasks'].append(__get_task_name_and_id(task))
        petitioner_list.append(petitioner)
    return petitioner_list, volunteer_list


def fetch_users_with_x_hours_until_task(hours_till_task):
    if not (hours_till_task and isinstance(hours_till_task, int)):
        raise Exception('Hours till task must be a legal int')
    curr_time = int(time.time())
    upto_due_date = curr_time + (hours_till_task * 60 * 60)
    filter = {
        'tasks': {
            '$elemMatch': {
                'due_date': {
                    '$gt': curr_time,
                    '$lt': upto_due_date
                }
            }
        }
    }
    cases = db.cases.find(filter=filter)
    cases = u.make_list(cases)
    petitioner_list, volunteer_list = __get_lists_from_cases(cases, upto_due_date)
    return petitioner_list, volunteer_list
