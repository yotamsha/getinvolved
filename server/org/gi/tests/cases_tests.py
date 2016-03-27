import json
import time
import unittest

import requests
from misc import _remove_from_db, _load, _push_to_db, MONGO, SERVER_URL_API, ACCESS_TOKEN_AUTH, validate_server_is_up
from org.gi.server import utils as utils
from org.gi.server.model.Task import ALL_TASKS_SAME_STATE_TRANSITION
from org.gi.server.service.notification.fetch_users_to_notify import fetch_users_with_upto_x_hours_until_task
from org.gi.server.validation.task.task_state_machine import TASK_UNDEFINED, TASK_ASSIGNED, TASK_COMPLETED, \
    TASK_PENDING, \
    TASK_ATTENDANCE_CONFIRMED
from org.gi.tests.users_tests import CONFIG_DATA_DIRECTORY as USER_CONFIG_DATA_DIRECTORY
import org.gi.server.validation.case_state_machine
from org.gi.server.validation.case_state_machine import CASE_PARTIALLY_ASSIGNED

__author__ = 'avishayb'

CONFIG_DATA_DIRECTORY = 'case_api'
DUE_DATE_HOURS = 25


class TestGIServerCaseTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestGIServerCaseTestCase, self).__init__(*args, **kwargs)
        self.config_folder = CONFIG_DATA_DIRECTORY
        self.users = _load('users.json', USER_CONFIG_DATA_DIRECTORY)
        self.cases = _load('cases.json', CONFIG_DATA_DIRECTORY)

    def setUp(self):
        _remove_from_db(MONGO, 'users')
        _remove_from_db(MONGO, 'cases')
        self.user_ids = _push_to_db(MONGO, 'users', self.users)
        self.case_ids = _push_to_db(MONGO, 'cases', self.cases)

    def _get_inserted_case(self):
        case = self._get_case()
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        return json.loads(r.content)

    def _get_case(self):
        case = _load('case_with_tasks.json', CONFIG_DATA_DIRECTORY)
        self._replace(case)
        return case

    @classmethod
    def setUpClass(cls):
        validate_server_is_up()

    def tearDown(self):
        _remove_from_db(MONGO, 'users')
        _remove_from_db(MONGO, 'cases')

    def prepare_and_push_to_db(self):
        _push_to_db(MONGO, 'users', self.users)
        r = requests.get('%s/users' % SERVER_URL_API, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        db_users = r.json()['users']
        for case in self.cases:
            case['petitioner_id'] = db_users[0]['id']
            for count, task in enumerate(case['tasks']):
                task['volunteer_id'] = db_users[count]['id']
                task['due_date'] = int(time.time()) + 4 * 60 * 60 + count
        _push_to_db(MONGO, 'cases', self.cases)
        return db_users

    def _replace(self, case):
        if case['petitioner_id'] == '__REPLACE__':
            case['petitioner_id'] = self.user_ids[0]
        if case.get('tasks'):
            for count, task in enumerate(case['tasks']):
                if 'volunteer_id' in task and task['volunteer_id'] == '__REPLACE__':
                    if count < len(self.user_ids):
                        task['volunteer_id'] = self.user_ids[count + 1]
                    else:
                        task['volunteer_id'] = self.user_ids[0]
                task['due_date'] = int(time.time()) + DUE_DATE_HOURS * 60 * 60 + count

    # positives

    def test_validate_location(self):
        pass

    def test_create_general_task_with_address(self):
        case = _load('case_with_general_task_with_address.json', self.config_folder)
        self._replace(case)
        stam=ACCESS_TOKEN_AUTH
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)

    def test_update_case_with_valid_state(self):
        states = [org.gi.server.validation.case_state_machine.CASE_PENDING_APPROVAL,
                  org.gi.server.validation.case_state_machine.CASE_PENDING_INVOLVEMENT,
                  org.gi.server.validation.case_state_machine.CASE_PARTIALLY_ASSIGNED,
                  org.gi.server.validation.case_state_machine.CASE_ASSIGNED,
                  org.gi.server.validation.case_state_machine.CASE_PARTIALLY_COMPLETED]
        for state in states:
            case = {"state": state}
            r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
            self.assertEqual(r.status_code, utils.HTTP_OK)

    def test_update_state_transitions(self):
        case = _load('case_state_transitions_4.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        case['state'] = 'cancelled_by_admin'
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)

    def test_inserted_case_and_task_state(self):
        # SETUP
        case_with_tasks = _load('case_with_tasks.json', self.config_folder)
        self._replace(case_with_tasks)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case_with_tasks, auth=ACCESS_TOKEN_AUTH)
        case_id = json.loads(r.content)['id']

        # TEST
        inserted_case = _get_case_from_db(case_id)
        self.assertEqual(inserted_case['state'], org.gi.server.validation.case_state_machine.CASE_PENDING_APPROVAL)
        for task in inserted_case['tasks']:
            self.assertEqual(task['state'], TASK_PENDING)

    def _case_tasks_transitions(self, use_valid_duration=True):
        # SETUP
        case_with_tasks = _load('case_with_tasks.json', self.config_folder)
        self._replace(case_with_tasks)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case_with_tasks, auth=ACCESS_TOKEN_AUTH)
        inserted_case = json.loads(r.content)
        case_id = inserted_case['id']
        case_tasks = {'tasks': inserted_case['tasks']}

        # TEST
        for state in [TASK_ASSIGNED, TASK_ATTENDANCE_CONFIRMED, TASK_COMPLETED]:
            for task in case_tasks['tasks']:
                task['state'] = state
                if state == TASK_COMPLETED and use_valid_duration:
                    task['duration'] = 300
            r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_id), json=case_tasks, auth=ACCESS_TOKEN_AUTH)
            if use_valid_duration:
                self.assertEqual(utils.HTTP_OK, r.status_code)
            else:
                if state == TASK_COMPLETED:
                    self.assertEqual(utils.HTTP_BAD_INPUT, r.status_code)
                else:
                    self.assertEqual(utils.HTTP_OK, r.status_code)
            r = requests.get('%s/cases/%s' % (SERVER_URL_API, case_id), auth=ACCESS_TOKEN_AUTH)
            if state != TASK_COMPLETED:
                self.assertEqual(r.json()['state'], ALL_TASKS_SAME_STATE_TRANSITION[state].encode('utf-8'))

    def test_case_tasks_transitions(self):
        self._case_tasks_transitions()

    def test_case_tasks_transitions_no_duration(self):
        self._case_tasks_transitions(use_valid_duration=False)

    def test_case_assign_user_to_task(self):
        # SETUP
        case = self._get_inserted_case()
        task = case['tasks'][0]
        task['state'] = TASK_ASSIGNED
        task['volunteer_id'] = self.user_ids[3]

        # TEST
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case['id']), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(utils.HTTP_OK, r.status_code)
        case = _get_case_from_db(case['id'])
        task = case['tasks'][0]
        self.assertEqual(self.user_ids[3], task['volunteer_id'])
        self.assertEqual(TASK_ASSIGNED, task['state'])
        self.assertEqual(CASE_PARTIALLY_ASSIGNED, case['state'])

    def test_create_case_fake_volunteer_id(self):
        case = _load('case_fake_volunteer_id.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)

    def test_create_case(self):
        case = _load('case_undefined.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)

    def test_cases_count(self):
        r = requests.get('%s/cases?count=1' % SERVER_URL_API, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        self.assertEqual(len(self.case_ids), r.json()['count'])

    def test_cases_count_mix_with_projection(self):
        r = requests.get('%s/cases?count=1&projection=a,b,c' % SERVER_URL_API, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_cases_count_mix_with_sort(self):
        r = requests.get(
            '%s/cases?count=1&sort=[(\'first_name\',\'ASCENDING\'),(\'last_name\',\'DESCENDING\')]' % SERVER_URL_API,
            auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_cases_invalid_query_args(self):
        r = requests.get(
            '%s/cases?count=1&zuzu=[(\'first_name\',\'ASCENDING\'),(\'last_name\',\'DESCENDING\')]' % SERVER_URL_API,
            auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_case_with_location(self):
        case = self._get_case()
        case['location'] = {
            'geo_location': {
                'lat': 30.0,
                'lng': 30.0
            }
        }
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)

    def test_get_cases_near_coord_and_by_distance(self):
        case = self._get_case()
        increment_latitude = 0.5
        base_lat = 32.0
        for i in range(0, 5):
            case['location'] = {
                'geo_location': {
                    'lng': 30.0,
                    'lat': base_lat + (i * increment_latitude)
                }
            }
            r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
            self.assertEqual(r.status_code, utils.HTTP_CREATED)
        near_query = {
            "location.geo_location":
                {"$near":
                     {
                         "$geometry": {
                             "type": "Point",
                             "coordinates": [30.00, 29.5]
                         },
                         "$maxDistance": 10000000
                     }
                 }
        }
        r = requests.get('%s/cases?filter=%s' % (SERVER_URL_API, near_query), auth=ACCESS_TOKEN_AUTH)
        cases = json.loads(r.content)
        self.assertTrue(len(cases) >= 1)
        for i in range(0, 5):
            self.assertEqual(base_lat + (i * increment_latitude), cases[i]['location']['geo_location']['lat'])

    # negatives

    def test_cannot_insert_case_with_due_date(self):
        case = _load('case_undefined.json', self.config_folder)
        self._replace(case)
        case['due_date'] = int(time.time()) + DUE_DATE_HOURS * 60 * 60
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_cannot_case_assign_user_with_same_id(self):
        # SETUP
        case = self._get_inserted_case()
        task = case['tasks'][0]
        task['state'] = TASK_ASSIGNED
        task['volunteer_id'] = self.user_ids[0]

        # TEST
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case['id']), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(utils.HTTP_BAD_INPUT, r.status_code)

    def test_case_too_far(self):
        case = self._get_case()
        case['location'] = {
            'geo_location': {
                'lat': 30.0,
                'lng': 30.0
            }
        }
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)
        near_query = {
            "location.geo_location":
                {"$near":
                     {
                         "$geometry": {
                             "type": "Point",
                             "coordinates": [40, 40]
                         },
                         "$maxDistance": 100
                     }
                 }
        }
        r = requests.get('%s/cases?filter=%s' % (SERVER_URL_API, near_query), auth=ACCESS_TOKEN_AUTH)
        cases = json.loads(r.content)
        self.assertTrue(len(cases) == 0)

    def test_create_cases_with_bad_transport_tasks(self):
        cases = _load('cases_with_bad_transportation_task.json', self.config_folder)
        for case in cases:
            self._replace(case)
            r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
            self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_case_fake_petitioner_id(self):
        case = _load('case_fake_petitioner_id.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_case_short_description(self):
        case = _load('case_short_description.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_case_dummy_property(self):
        case = _load('case_dummy_property.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_transportation_case(self):
        case = _load('case_with_transportation_task.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)

    def test_create_transportation_case_wrong_country_code(self):
        case = _load('case_with_transportation_task_wrong_country_code.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_transportation_case_short_city(self):
        case = _load('case_with_transportation_task_short_city.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_transportation_case_long_city(self):
        case = _load('case_with_transportation_task_long_city.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_case_wrong_task_type(self):
        case = _load('case_with_wrong_task_type.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_case_no_task_type(self):
        case = _load('case_with_no_task_type.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_case_no_tasks(self):
        case = _load('case_with_no_tasks.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_create_transportation_case_dummy_property(self):
        case = _load('case_with_transportation_task_dummy_property.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_update_case_with_invalid_state(self):
        case = _load('case_state_transitions_1.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)
        case = _load('case_state_transitions_2.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_update_case_to_completed_but_tasks_are_not_completed(self):
        case = _load('case_state_transitions_3.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)
        case = _load('case_state_transitions_5.json', self.config_folder)
        self._replace(case)
        db = MONGO.get_default_database()
        result = db.cases.update_one({"tasks.state": TASK_UNDEFINED},
                                     {'$set': {'state': org.gi.server.validation.case_state_machine.CASE_ASSIGNED,
                                               'tasks.$.state': TASK_ASSIGNED}})
        self.assertEqual(result.modified_count, 1)
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_bad_task_update(self):
        case_with_tasks = _load('case_with_tasks.json', self.config_folder)
        self._replace(case_with_tasks)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case_with_tasks, auth=ACCESS_TOKEN_AUTH)
        inserted_case = json.loads(r.content)
        case_id = inserted_case['id']
        case_tasks = {'tasks': inserted_case['tasks']}
        case_tasks['tasks'][0]['state'] = TASK_ASSIGNED
        case_tasks['tasks'][1]['state'] = TASK_ASSIGNED
        del case_tasks['tasks'][-1]
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_id), json=case_tasks, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(utils.HTTP_OK, r.status_code)

        case_tasks = {}
        for task in _get_case_from_db(case_id)['tasks']:
            if task['state'] == TASK_ASSIGNED:
                task['state'] = TASK_COMPLETED
                case_tasks['tasks'] = [task]
                break
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_id), json=case_tasks, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(utils.HTTP_BAD_INPUT, r.status_code)

    def test_not_deleting_tasks_on_update(self):
        case_with_tasks = _load('case_with_tasks.json', self.config_folder)
        self._replace(case_with_tasks)
        orig_num_tasks = len(case_with_tasks['tasks'])
        r = requests.post('%s/cases' % SERVER_URL_API, json=case_with_tasks, auth=ACCESS_TOKEN_AUTH)
        inserted_case = json.loads(r.content)
        case_id = inserted_case['id']
        case_update = {'tasks': [inserted_case['tasks'][0]]}
        case_update['tasks'][0]['state'] = TASK_ASSIGNED
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_id), json=case_update, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(utils.HTTP_OK, r.status_code)
        updated_case = {'tasks': _get_case_from_db(case_id)['tasks']}
        self.assertEqual(orig_num_tasks, len(updated_case.get('tasks')))

    # fetching user notifications is related to cases/tasks
    def test_fetch_users_to_notify(self):
        self._get_inserted_case()
        petitioner_list, volunteer_list = fetch_users_with_upto_x_hours_until_task(DUE_DATE_HOURS + 1)
        self.assertTrue(len(petitioner_list) == 1)
        petitioner = petitioner_list[0]
        self.assertTrue(petitioner.get('case_title'))
        self.assertTrue(petitioner.get('details'))
        self.assertTrue(petitioner.get('user_id'))
        self.assertTrue(len(petitioner.get('tasks')) == 3)
        self.assertTrue(len(volunteer_list) == 3)
        for volunteer in volunteer_list:
            self.assertTrue(volunteer.get('case_title'))
            self.assertTrue(volunteer.get('details'))
            self.assertTrue(volunteer.get('user_id'))
            self.assertTrue(len(volunteer.get('tasks')) == 1)

    def test_fetch_users_return_none(self):
        self._get_inserted_case()
        petitioner_list, volunteer_list = fetch_users_with_upto_x_hours_until_task(DUE_DATE_HOURS - 1)
        self.assertTrue(len(petitioner_list) == 0)
        self.assertTrue(len(volunteer_list) == 0)

    def test_count_header(self):
        r = requests.get('%s/cases' % (SERVER_URL_API), auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        self.assertTrue(utils.COUNT_HEADER in r.headers)



    def test_ticket_230(self):
        case_with_tasks = _load('case_with_tasks_ticket_230.json', self.config_folder)
        self._replace(case_with_tasks)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case_with_tasks, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)
        case_from_server = r.json()
        for task in case_from_server['tasks']:
            del task['description']
        case_from_server['tasks'][0]['state'] = 'assigned'
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_from_server['id']), json=case_from_server,
                         auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        case_from_server = r.json()
        for task in case_from_server['tasks']:
            task['description'] = 'A description....'
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_from_server['id']), json=case_from_server,
                         auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        r = requests.get('%s/cases/%s' % (SERVER_URL_API, case_from_server['id']), auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        self.assertTrue(r.json()['tasks'][0]['description'] is not None)

    def test_add_volunteer_attributes_not_lazy(self):
        case = self._fetch_case_with_volunteer_attributes(lazy=False)
        for task in case['tasks']:
            self.assertTrue(isinstance(task['volunteer'], dict))
            self.assertTrue(isinstance(task['volunteer_id'], (str, unicode)))

    def test_add_volunteer_attributes_lazy(self):
        case = self._fetch_case_with_volunteer_attributes()
        for task in case['tasks']:
            self.assertTrue(isinstance(task['volunteer_id'], (str, unicode)))
            self.assertTrue(task.get('volunteer') is None)

    def _fetch_case_with_volunteer_attributes(self, lazy=True):
        case = self._get_case()
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)
        if lazy:
            r = requests.get('%s/cases/%s' % (SERVER_URL_API, r.json()['id']), auth=ACCESS_TOKEN_AUTH)
        else:
            r = requests.get('%s/cases/%s?add_volunteer_attributes=%s' % (SERVER_URL_API, r.json()['id'], 'yes'),
                             auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        return r.json()

    def test_ticket_256(self):
        case_with_tasks = _load('case_ticket_256.json', self.config_folder)
        self._replace(case_with_tasks)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case_with_tasks, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)
        case_from_server = r.json()
        case_from_server['tasks'][0]['volunteer_id'] = self.user_ids[1]
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_from_server['id']), json=case_from_server,
                         auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        self.assertEqual(r.json()['state'], org.gi.server.validation.case_state_machine.CASE_ASSIGNED)
        self.assertEqual(r.json()['tasks'][0]['state'], TASK_ASSIGNED)

    def test_ticket_246(self):
        """
        Make sure the server is not going to try and validate non existing fields on update operations
        """
        case_with_tasks = _load('case_with_tasks_ticket_246.json', self.config_folder)
        self._replace(case_with_tasks)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case_with_tasks, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)
        case_from_server = r.json()
        del case_from_server['description']
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_from_server['id']), json=case_from_server,
                         auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        case_from_server = r.json()
        del case_from_server['state']
        for task in case_from_server['tasks']:
            del task['description']
            del task['state']
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_from_server['id']), json=case_from_server,
                         auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_OK)

    def test_bad_http_methods(self):
        r = requests.delete('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_METHOD_NOT_ALLOWED)

def _get_case_from_db(case_id):
    r = requests.get('%s/cases/%s' % (SERVER_URL_API, case_id), auth=ACCESS_TOKEN_AUTH)
    inserted_case = json.loads(r.content)
    return inserted_case
