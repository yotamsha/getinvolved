import unittest
import json
import sys
import os
import time

import requests
import pymongo

from org.gi.server import validations as v

from org.gi.config import config


DB_URI = config.get_db_uri()
SERVER_URL = 'http://localhost:5000/api'
MONGO = pymongo.MongoClient(DB_URI)


class GIAddressValidationTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIAddressValidationTestCase, self).__init__(*args, **kwargs)
        self.config_folder = 'address'

    def test_address(self):
        addr = _load('empty_address.json', self.config_folder)
        faults = []
        v.validate_address(addr, faults)
        self.assertEqual(len(faults), 1)

    def test_half_address(self):
        addr = _load('half_empty_address.json', self.config_folder)
        faults = []
        v.validate_address(addr, faults)
        self.assertEqual(len(faults), 1)

    def test_wrong_country(self):
        addr = _load('wrong_country_address.json', self.config_folder)
        faults = []
        v.validate_address(addr, faults)
        self.assertEqual(len(faults), 1)

    def test_address_ok(self):
        addr = _load('address.json', self.config_folder)
        faults = []
        v.validate_address(addr, faults)
        self.assertEqual(len(faults), 0)


class GIServerCaseTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIServerCaseTestCase, self).__init__(*args, **kwargs)
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
        r = requests.get('%s/users' % SERVER_URL)
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
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_case_fake_volunteer_id(self):
        case = _load('case_fake_volunteer_id.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 201)

    def test_create_case(self):
        case = _load('case_undefined.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 201)

    def test_create_case_short_description(self):
        case = _load('case_short_description.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_case_dummy_property(self):
        case = _load('case_dummy_property.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_transportation_case(self):
        case = _load('case_with_transportation_task.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 201)

    def test_create_transportation_case_wrong_country_code(self):
        case = _load('case_with_transportation_task_wrong_country_code.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_transportation_case_short_city(self):
        case = _load('case_with_transportation_task_short_city.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_transportation_case_long_city(self):
        case = _load('case_with_transportation_task_long_city.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_case_wrong_task_type(self):
        case = _load('case_with_wrong_task_type.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_case_no_task_type(self):
        case = _load('case_with_no_task_type.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_case_no_tasks(self):
        case = _load('case_with_no_tasks.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_transportation_case_dummy_property(self):
        case = _load('case_with_transportation_task_dummy_property.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 400)

    def test_create_general_task_with_address(self):
        case = _load('case_with_general_task_with_address.json', self.config_folder)
        self._replace(case)
        r = requests.post('%s/cases' % SERVER_URL, json=case)
        self.assertEqual(r.status_code, 201)

    def test_update_case_with_invalid_state(self):
        case = _load('case_state_transitions_1.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case)
        self.assertEqual(r.status_code, 400)

    def test_update_case_with_valid_state(self):
        case = _load('case_state_transitions_2.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case)
        self.assertEqual(r.status_code, 400)

    def test_update_case_to_completed(self):
        case = _load('case_state_transitions_3.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case)
        self.assertEqual(r.status_code, 400)

    def test_update_case_to_pending_approval(self):
        case = _load('case_state_transitions_4.json', self.config_folder)
        self._replace(case)
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case)
        self.assertEqual(r.status_code, 204)
        #
        # keep on testing the state machine
        #
        case['state'] = 'cancelled_by_admin'
        r = requests.put('%s/cases/%s' % (SERVER_URL, self.case_ids[0]), json=case)
        self.assertEqual(r.status_code, 204)

class GIServerUsersTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIServerUsersTestCase, self).__init__(*args, **kwargs)
        self.config_folder = 'user'
        self.users = _load('users.json', self.config_folder)

    def setUp(self):
        _remove_from_db(MONGO, 'users')
        self.ids = _push_to_db(MONGO, 'users', self.users)

    def tearDown(self):
        _remove_from_db(MONGO, 'users')


    def test_has_users_db(self):
        try:
            r = requests.get('%s/users' % SERVER_URL)
            self.assertEqual(r.status_code, 200)
            db_users = r.json()
            self.assertEqual(len(db_users), len(self.users))
            user_names = [usr['user_name'] for usr in self.users]
            for usr in db_users:
                self.assertTrue(usr['user_name'] in user_names)
        except Exception:
            _remove_from_db(MONGO, 'users')

    def test_sort_asc(self):
        r = requests.get('%s/users?sort=[(\'user_name\',\'ASCENDING\')]' % SERVER_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]['user_name'], 'Ajack')

    def test_sort_desc(self):
        r = requests.get('%s/users?sort=[(\'user_name\',\'DESCENDING\')]' % SERVER_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]['user_name'], 'Gboon')

    def test_projection(self):
        r = requests.get('%s/users?projection=user_name,email' % SERVER_URL)
        self.assertTrue(r.status_code, 200)
        self.assertTrue(r.json()[0].get('user_name') is not None)
        self.assertTrue(r.json()[0].get('email') is not None)
        self.assertTrue(r.json()[0].get('password') is None)
        self.assertTrue(r.json()[0].get('phone_number') is None)

    def test_paging(self):
        PAGE_SIZE = 2
        counter = 0
        usr_counter = 0
        loop = True
        while loop:
            r = requests.get('%s/users?sort=[(\'user_name\',\'ASCENDING\')]&page_size=%d&page_number=%d' % (
                SERVER_URL, PAGE_SIZE, counter))
            loop = len(r.json())
            counter += 1
            self.assertTrue(r.status_code, 200)
            for usr in r.json():
                self.assertTrue(usr['user_name'] in [_usr['user_name'] for _usr in self.users])
            usr_counter += len(r.json())
            self.assertTrue(len(r.json()) <= PAGE_SIZE)

        self.assertEqual(usr_counter, len(self.users),
                         'Expecting to return %d users from server. Only %d users were returned.' % (
                         len(self.users), usr_counter))


    def test_filter_or(self):
        emails = ['dan@gi.net', 'jack@gi.net']
        _filter = '{"$or":[{"email":{"$eq":"%s"}},{"email":{"$eq":"%s"}}]}' % (emails[0], emails[1])
        r = requests.get('%s/users?filter=%s' % (SERVER_URL, _filter))
        self.assertTrue(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)
        for user in r.json():
            self.assertTrue(user['email'] in emails)

    def test_filter_and(self):
        emails = ['dan@gi.net', 'jack@gi.net']
        _filter = '{"$and":[{"email":{"$eq":"%s"}},{"email":{"$eq":"%s"}}]}' % (emails[0], emails[1])
        r = requests.get('%s/users?filter=%s' % (SERVER_URL, _filter))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_filter_ne(self):
        _filter = '{ "email": { "$ne": "dan@gi.net" }}'
        r = requests.get('%s/users?filter=%s' % (SERVER_URL, _filter))
        self.assertTrue(r.status_code, 200)
        self.assertEqual(len(r.json()), len(self.users) - 1)


    def test_empty_payload(self):
        r = requests.post('%s/users' % SERVER_URL, json=json.dumps({}))
        self.assertEqual(r.status_code, 400)


    def test_wrong_email(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('wrong_email.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_wrong_phone_number(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('wrong_phone_number.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_short_password(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('short_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_long_password(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('long_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_no_first_name(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('no_first_name.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_delete_one(self):
        try:
            r = requests.delete('%s/users/%s' % (SERVER_URL, self.ids[0]))
            self.assertEqual(r.status_code, 204)
        except Exception:
            _remove_from_db(MONGO, 'users')

    def test_delete_wrong_user_id(self):
        r = requests.delete('%s/users/%s' % (SERVER_URL, 'qazxswedc'))
        self.assertEqual(r.status_code, 404)

    def test_empty_payload_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]), json=json.dumps({}))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')

    def test_wrong_email_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         json=_load('wrong_email.json', self.config_folder))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')

    def test_wrong_phone_number_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         json=_load('wrong_phone_number.json', self.config_folder))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')


    def test_short_password_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         json=_load('short_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')


    def test_long_password_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         json=_load('long_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')


    def test_no_first_name_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         json=_load('no_first_name.json', self.config_folder))
        self.assertEqual(r.status_code, 400)

    def test_create_a_user(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('a_user.json', self.config_folder))
        self.assertEqual(r.status_code, 201)
        pushed_to_api = _load('a_user.json', self.config_folder)
        created = r.json();
        for k, v in pushed_to_api.iteritems():
            self.assertEqual(v, created[k])

    def test_create_a_user_with_roles(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('a_user_with_roles.json', self.config_folder))
        self.assertEqual(r.status_code, 201)
        pushed_to_api = _load('a_user_with_roles.json', self.config_folder)
        created = r.json();
        for k, v in pushed_to_api.iteritems():
            self.assertEqual(v, created[k])

    def test_create_a_user_with_wrong_roles(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('a_user_with_wrong_roles.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_create_a_user_with_int_pwd(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('a_user_with_int_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)

    def test_create_a_user_with_str_phone_num(self):
        r = requests.post('%s/users' % SERVER_URL, json=_load('a_user_with_str_phone_number.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


def _get_id(self):
    _push_to_db(MONGO, 'users', self.users)
    r = requests.get('%s/users' % SERVER_URL)
    self.assertEqual(r.status_code, 200)
    return r.json()['users'][0]['id']


def _load(file_name, folder_name):
    path = sys.modules[__name__].__file__
    path = path[:path.rfind(os.path.sep)]
    with open('%s/config/%s/%s' % (path, folder_name, file_name)) as data_file:
        return json.load(data_file)


def _push_to_db(mongo, collection_name, data):
    db = mongo.get_default_database()
    db[collection_name].insert_many(data)
    return _get_ids(mongo, collection_name)


def _remove_from_db(mongo, collection_name):
    db = mongo.get_default_database()
    db[collection_name].drop()


def _get_ids(mongo, collection_name):
    db = mongo.get_default_database()
    records = db[collection_name].find()
    return [str(r['_id']) for r in records]
