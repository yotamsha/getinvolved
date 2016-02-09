__author__ = 'avishayb'
import requests
import unittest
import time
from misc import _remove_from_db, _load, _push_to_db, MONGO, SERVER_URL, AUTH
from org.gi.server import validations as v

class TestGIServerCaseTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestGIServerCaseTestCase, self).__init__(*args, **kwargs)
        self.config_folder = 'case'
        self.users = _load('users.json', 'user')
        self.cases = _load('cases.json', 'case')

    def setUp(self):
        _remove_from_db(MONGO, 'users')
        _remove_from_db(MONGO, 'cases')
        self.user_ids = _push_to_db(MONGO, 'users', self.users)
        self.case_ids = _push_to_db(MONGO, 'cases', self.cases)


    def tearDown(self):
        _remove_from_db(MONGO, 'users')
        _remove_from_db(MONGO, 'cases')


    def prepare_and_push_to_db(self):
        _push_to_db(MONGO, 'users', self.users)
        r = requests.get('%s/users' % SERVER_URL, auth=AUTH)
        self.assertEqual(r.status_code, 200)
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
                if task['volunteer_id'] == '__REPLACE__':
                    task['volunteer_id'] = self.user_ids[count]
                task['due_date'] = int(time.time()) + 4 * 60 * 60 + count

    def test_create_case_fake_petitioner_id(self):
        case = _load('case_fake_petitioner_id.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_case_fake_volunteer_id(self):
        case = _load('case_fake_volunteer_id.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 201)

    def test_create_case(self):
        case = _load('case_undefined.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 201)

    def test_create_case_short_description(self):
        case = _load('case_short_description.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_case_dummy_property(self):
        case = _load('case_dummy_property.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_transportation_case(self):
        case = _load('case_with_transportation_task.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 201)

    def test_create_transportation_case_wrong_country_code(self):
        case = _load('case_with_transportation_task_wrong_country_code.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_transportation_case_short_city(self):
        case = _load('case_with_transportation_task_short_city.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_transportation_case_long_city(self):
        case = _load('case_with_transportation_task_long_city.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_case_wrong_task_type(self):
        case = _load('case_with_wrong_task_type.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_case_no_task_type(self):
        case = _load('case_with_no_task_type.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_case_no_tasks(self):
        case = _load('case_with_no_tasks.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_transportation_case_dummy_property(self):
        case = _load('case_with_transportation_task_dummy_property.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_create_general_task_with_address(self):
        case = _load('case_with_general_task_with_address.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case, auth=AUTH)
        self.assertEqual(r.status_code, 201)

    def test_update_case_with_invalid_state(self):
        case = _load('case_state_transitions_1.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_update_case_with_valid_state(self):
        case = _load('case_state_transitions_2.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_update_case_to_completed(self):
        case = _load('case_state_transitions_3.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_update_case_to_completed_but_tasks_are_not_completed(self):
        case = _load('case_state_transitions_5.json', self.config_folder)
        self._replace(case)
        db = MONGO.get_default_database()
        result = db.cases.update_one({"tasks.state": v.TASK_UNDEFINED},
                                     {'$set': {'state': v.CASE_ASSIGNED, 'tasks.$.state': v.TASK_ASSIGNED}})
        self.assertEqual(result.modified_count, 1)
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case, auth=AUTH)
        self.assertEqual(r.status_code, 400)

    def test_update_state_transitions(self):
        case = _load('case_state_transitions_4.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case, auth=AUTH)
        self.assertEqual(r.status_code, 204)
        #
        # keep on testing the state machine
        #
        case['state'] = 'cancelled_by_admin'
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case, auth=AUTH)
        self.assertEqual(r.status_code, 204)

    def test_delete_case(self):
        r = requests.delete('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), auth=AUTH)
        self.assertEqual(r.status_code, 204)

    def test_delete_case_wrong_id(self):
        wrong_id = self.case_ids[0].replace(self.case_ids[0][0], str(int(self.case_ids[0][0]) + 1))
        r = requests.delete('%s/cases/%s' % (SERVER_URL, wrong_id), auth=AUTH)
        self.assertEqual(r.status_code, 404)

