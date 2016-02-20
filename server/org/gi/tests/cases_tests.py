import json
import time
import unittest

import requests

import org.gi.server.validation.case_state_machine
from misc import _remove_from_db, _load, _push_to_db, MONGO, SERVER_URL_API, ACCESS_TOKEN_AUTH, validate_server_is_up
from org.gi.server import utils as utils
from org.gi.server.model.Task import ALL_TASKS_SAME_STATE_TRANSITION
from org.gi.server.validation.task.task_state_machine import TASK_UNDEFINED, TASK_ASSIGNED, TASK_COMPLETED, TASK_PENDING
from org.gi.tests.users_tests import CONFIG_DATA_DIRECTORY as USER_CONFIG_DATA_DIRECTORY
__author__ = 'avishayb'

CONFIG_DATA_DIRECTORY = 'case_api'


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
                    task['volunteer_id'] = self.user_ids[count]
                task['due_date'] = int(time.time()) + 4 * 60 * 60 + count

    # positives

    def test_validate_location(self):
        pass

    def test_create_general_task_with_address(self):
        case = _load('case_with_general_task_with_address.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)

    def test_update_case_with_valid_state(self):
        states = [org.gi.server.validation.case_state_machine.CASE_PENDING_APPROVAL, org.gi.server.validation.case_state_machine.CASE_PENDING_INVOLVEMENT, org.gi.server.validation.case_state_machine.CASE_PARTIALLY_ASSIGNED, org.gi.server.validation.case_state_machine.CASE_ASSIGNED,
                  org.gi.server.validation.case_state_machine.CASE_PARTIALLY_COMPLETED]
        for state in states:
            case = {"state": state}
            r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
            self.assertEqual(r.status_code, utils.HTTP_NO_CONTENT)

    def test_delete_case(self):
        r = requests.delete('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_NO_CONTENT)

    def test_update_state_transitions(self):
        case = _load('case_state_transitions_4.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_NO_CONTENT)
        case['state'] = 'cancelled_by_admin'
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_NO_CONTENT)

    def test_inserted_case_and_task_state(self):
        # SETUP
        case_with_tasks = _load('case_with_tasks.json', self.config_folder)
        self._replace(case_with_tasks)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case_with_tasks, auth=ACCESS_TOKEN_AUTH)
        case_id = json.loads(r.content)['id']

        # TEST
        inserted_case = self._get_case(case_id)
        self.assertEqual(inserted_case['state'], org.gi.server.validation.case_state_machine.CASE_PENDING_APPROVAL)
        for task in inserted_case['tasks']:
            self.assertEqual(task['state'], TASK_PENDING)

    def _get_case(self, case_id):
        r = requests.get('%s/cases/%s' % (SERVER_URL_API, case_id), auth=ACCESS_TOKEN_AUTH)
        inserted_case = json.loads(r.content)
        return inserted_case

    def test_task_transitions(self):
        # SETUP
        case_with_tasks = _load('case_with_tasks.json', self.config_folder)
        self._replace(case_with_tasks)
        r = requests.post('%s/cases' % SERVER_URL_API, json=case_with_tasks, auth=ACCESS_TOKEN_AUTH)
        inserted_case = json.loads(r.content)
        case_id = inserted_case['id']
        case_tasks = {'tasks': inserted_case['tasks']}

        # TEST
        task_states = [TASK_ASSIGNED, TASK_COMPLETED]
        for state in task_states:
            for task in case_tasks['tasks']:
                task['state'] = state
            r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_id), json=case_tasks, auth=ACCESS_TOKEN_AUTH)
            self.assertEqual(utils.HTTP_NO_CONTENT, r.status_code)
            r = requests.get('%s/cases/%s' % (SERVER_URL_API, case_id), auth=ACCESS_TOKEN_AUTH)
            self.assertEqual(json.loads(r.content)['state'], ALL_TASKS_SAME_STATE_TRANSITION[state])

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

    def test_create_case_with_location(self):
        case = _get_case(self)
        case['location'] = {
            'geo_location': {
                'lat': 30.0,
                'lng': 30.0
            }
        }
        r = requests.post('%s/cases' % SERVER_URL_API, json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_CREATED)


    # negatives

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
                                     {'$set': {'state': org.gi.server.validation.case_state_machine.CASE_ASSIGNED, 'tasks.$.state': TASK_ASSIGNED}})
        self.assertEqual(result.modified_count, 1)
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, self.case_ids[0]), json=case, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_BAD_INPUT)

    def test_delete_case_wrong_id(self):
        wrong_id = self.case_ids[0].replace(self.case_ids[0][0], str(int(self.case_ids[0][0]) + 1))
        r = requests.delete('%s/cases/%s' % (SERVER_URL_API, wrong_id), auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(r.status_code, utils.HTTP_NOT_FOUND)

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
        self.assertEqual(utils.HTTP_NO_CONTENT, r.status_code)

        case_tasks = {}
        for task in self._get_case(case_id)['tasks']:
            if task['state'] == TASK_ASSIGNED:
                task['state'] = TASK_COMPLETED
                case_tasks['tasks'] = [task]
                break
        r = requests.put('%s/cases/%s' % (SERVER_URL_API, case_id), json=case_tasks, auth=ACCESS_TOKEN_AUTH)
        self.assertEqual(utils.HTTP_BAD_INPUT, r.status_code)
        self.assertTrue('A case cannot have the following states together' in r.content)

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
        self.assertEqual(utils.HTTP_NO_CONTENT, r.status_code)
        updated_case = {'tasks': self._get_case(case_id)['tasks']}
        self.assertEqual(orig_num_tasks, len(updated_case.get('tasks')))


def _get_case(test):
    case = _load('case_with_tasks.json', CONFIG_DATA_DIRECTORY)
    test._replace(case)
    return case

