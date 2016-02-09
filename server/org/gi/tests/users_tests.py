__author__ = 'avishayb'

import requests
from requests.auth import HTTPBasicAuth
import unittest
from misc import _remove_from_db, _load, _push_to_db, MONGO, SERVER_URL, AUTH
import org.gi.server.authorization as auth
import json

class GIServerUsersTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIServerUsersTestCase, self).__init__(*args, **kwargs)
        self.config_folder = 'user'
        self.users = _load('users.json', self.config_folder)
        self.passwords = {}

    def setUp(self):
        _remove_from_db(MONGO, 'users')
        for user in self.users:
            self.passwords[user['user_name']] = user['password']
            user['password'] = auth.hash_password(user['password'])
            # print(user['user_name'] + ', ' + user['password'] + ' , ' + self.passwords[user['user_name']])
        self.ids = _push_to_db(MONGO, 'users', self.users)

    def tearDown(self):
        _remove_from_db(MONGO, 'users')


    def test_has_users_db(self):
        try:
            r = requests.get('%s/users' % SERVER_URL, auth=AUTH)
            self.assertEqual(r.status_code, 200)
            db_users = r.json()
            self.assertEqual(len(db_users), len(self.users))
            user_names = [usr['user_name'] for usr in self.users]
            for usr in db_users:
                self.assertTrue(usr['user_name'] in user_names)
        except Exception:
            _remove_from_db(MONGO, 'users')

    def test_sort_asc(self):
        r = requests.get('%s/users?sort=[(\'user_name\',\'ASCENDING\')]' % SERVER_URL, auth=AUTH)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]['user_name'], 'Ajack')

    def test_sort_desc(self):
        r = requests.get('%s/users?sort=[(\'user_name\',\'DESCENDING\')]' % SERVER_URL, auth=AUTH)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]['user_name'], 'Gboon')

    def test_projection(self):
        r = requests.get('%s/users?projection=user_name,email' % SERVER_URL, auth=AUTH)
        self.assertTrue(r.status_code, 200)
        self.assertTrue(r.json()[0].get('user_name') is not None)
        self.assertTrue(r.json()[0].get('email') is not None)
        self.assertTrue(r.json()[0].get('password') is None)
        self.assertTrue(r.json()[0].get('phone_number') is None)

    def test_paging_no_sort(self):
        PAGE_SIZE = 2
        counter = 0
        usr_counter = 0
        loop = True
        while loop:
            r = requests.get('%s/users?page_size=%d&page_number=%d' % (
                SERVER_URL, PAGE_SIZE, counter), auth=AUTH)
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


    def test_paging(self):
        PAGE_SIZE = 2
        counter = 0
        usr_counter = 0
        loop = True
        while loop:
            r = requests.get('%s/users?sort=[(\'user_name\',\'ASCENDING\')]&page_size=%d&page_number=%d' % (
                SERVER_URL, PAGE_SIZE, counter), auth=AUTH)
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
        r = requests.get('%s/users?filter=%s' % (SERVER_URL, _filter), auth=AUTH)
        self.assertTrue(r.status_code, 200)
        self.assertEqual(len(r.json()), 2)
        for user in r.json():
            self.assertTrue(user['email'] in emails)

    def test_filter_and(self):
        emails = ['dan@gi.net', 'jack@gi.net']
        _filter = '{"$and":[{"email":{"$eq":"%s"}},{"email":{"$eq":"%s"}}]}' % (emails[0], emails[1])
        r = requests.get('%s/users?filter=%s' % (SERVER_URL, _filter), auth=AUTH)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    def test_filter_ne(self):
        _filter = '{ "email": { "$ne": "dan@gi.net" }}'
        r = requests.get('%s/users?filter=%s' % (SERVER_URL, _filter), auth=AUTH)
        self.assertTrue(r.status_code, 200)
        self.assertEqual(len(r.json()), len(self.users) - 1)


    def test_empty_payload(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH, json=json.dumps({}))
        self.assertEqual(r.status_code, 400)


    def test_wrong_email(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH, json=_load('wrong_email.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_wrong_phone_number(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH, json=_load('wrong_phone_number.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_short_password(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH, json=_load('short_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_long_password(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH, json=_load('long_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_no_first_name(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH, json=_load('no_first_name.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_delete_one(self):
        try:
            r = requests.delete('%s/users/%s' % (SERVER_URL, self.ids[0]), auth=AUTH)
            self.assertEqual(r.status_code, 204)
        except Exception:
            _remove_from_db(MONGO, 'users')

    def test_delete_wrong_user_id(self):
        r = requests.delete('%s/users/%s' % (SERVER_URL, 'qazxswedc'), auth=AUTH)
        self.assertEqual(r.status_code, 404)

    def test_empty_payload_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]), auth=AUTH, json=json.dumps({}))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')

    def test_wrong_email_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         auth=AUTH, json=_load('wrong_email.json', self.config_folder))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')

    def test_wrong_phone_number_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         auth=AUTH, json=_load('wrong_phone_number.json', self.config_folder))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')


    def test_short_password_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         auth=AUTH, json=_load('short_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')


    def test_long_password_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         auth=AUTH, json=_load('long_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)
        _remove_from_db(MONGO, 'users')


    def test_no_first_name_put(self):
        r = requests.put('%s/users/%s' % (SERVER_URL, self.ids[0]),
                         auth=AUTH, json=_load('no_first_name.json', self.config_folder))
        self.assertEqual(r.status_code, 400)

    def test_create_a_user(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH, json=_load('a_user.json', self.config_folder))
        self.assertEqual(r.status_code, 201)
        pushed_to_api = _load('a_user.json', self.config_folder)
        created = r.json();
        for k, v in pushed_to_api.iteritems():
            if k != 'password':
                self.assertEqual(v, created[k])

    def test_create_a_user_with_roles(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH, json=_load('a_user_with_roles.json', self.config_folder))
        self.assertEqual(r.status_code, 201)
        pushed_to_api = _load('a_user_with_roles.json', self.config_folder)
        created = r.json();
        for k, v in pushed_to_api.iteritems():
            if k != 'password':
                self.assertEqual(v, created[k])

    def test_create_a_user_with_wrong_roles(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH,
                          json=_load('a_user_with_wrong_roles.json', self.config_folder))
        self.assertEqual(r.status_code, 400)


    def test_create_a_user_with_int_pwd(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH,
                          json=_load('a_user_with_int_password.json', self.config_folder))
        self.assertEqual(r.status_code, 400)

    def test_create_a_user_with_str_phone_num(self):
        r = requests.post('%s/users' % SERVER_URL, auth=AUTH,
                          json=_load('a_user_with_str_phone_number.json', self.config_folder))
        self.assertEqual(r.status_code, 400)

    def test_create_a_user_wrong_user_password(self):
        _AUTH = HTTPBasicAuth('wrong', 'wrong')
        r = requests.post('%s/users' % SERVER_URL, auth=_AUTH,
                          json=_load('a_user_with_str_phone_number.json', self.config_folder))
        self.assertEqual(r.status_code, 401)

    @unittest.skip("Skipping... It needs to run under production mode")
    def test_create_a_user_with_real_credentials(self):
        _AUTH = HTTPBasicAuth(self.users[0]['user_name'], self.passwords.get(self.users[0]['user_name']))
        r = requests.post('%s/users' % SERVER_URL, auth=_AUTH,
                          json=_load('a_user.json', self.config_folder))
        self.assertEqual(r.status_code, 201)
        _AUTH = HTTPBasicAuth('u_cant_find_me_in_db', self.passwords.get(self.users[0]['user_name']))
        r = requests.post('%s/users' % SERVER_URL, auth=_AUTH,
                          json=_load('a_user.json', self.config_folder))
        self.assertEqual(r.status_code, 401)
