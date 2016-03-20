import unittest

from misc import _remove_from_db, _load, _push_to_db, MONGO, SERVER_URL, validate_server_is_up
import org.gi.server.authorization as auth
import org.gi.server.utils as utils

import requests


class GIAccessTokenAuthentication(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIAccessTokenAuthentication, self).__init__(*args, **kwargs)
        self.config_folder = 'auth'
        self._user = _load('user.json', self.config_folder)
        self.user_and_password = {
            'username': self._user['user_name'],
            'password': self._user['password']
        }
        # self._auth = HTTPBasicAuth(self._user['user_name'], self._user['password'])

    def setUp(self):
        _remove_from_db(MONGO, 'users')
        user = self._user.copy()
        user['password'] = auth.hash_password(user['password'])
        _push_to_db(MONGO, 'users', [user])

    @classmethod
    def setUpClass(cls):
        validate_server_is_up()

    def tearDown(self):
        _remove_from_db(MONGO, 'users')

    # positive

    def test_user_login(self):
        r = requests.get('%s/login' % SERVER_URL, params=self.user_and_password)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        r = requests.post('%s/login' % SERVER_URL, params=self.user_and_password)
        self.assertEqual(r.status_code, utils.HTTP_OK)
        r = requests.post('%s/login' % SERVER_URL, json=self.user_and_password)
        self.assertEqual(r.status_code, utils.HTTP_OK)


    def test_password_all_caps(self):
        details = self.user_and_password.copy()
        details['password'] = details['password'].upper()
        r = requests.post('%s/login' % SERVER_URL, params=details)
        self.assertEqual(r.status_code, utils.HTTP_UNAUTHORIZED)

    def test_user_all_caps(self):
        details = self.user_and_password.copy()
        details['username'] = details['username'].upper()
        r = requests.post('%s/login' % SERVER_URL, params=details)
        self.assertEqual(r.status_code, utils.HTTP_UNAUTHORIZED)

    def test_user_bad_password_login(self):
        details = self.user_and_password.copy()
        details['password'] += "lala"
        r = requests.get('%s/login' % SERVER_URL, params=details)
        self.assertEqual(utils.HTTP_UNAUTHORIZED, r.status_code)

    def test_missing_params(self):
        r = requests.get('%s/login' % SERVER_URL)
        self.assertEqual(r.status_code, utils.HTTP_UNAUTHORIZED)
        r = requests.get('%s/login' % SERVER_URL, params={'username': 'moshe'})
        self.assertEqual(r.status_code, utils.HTTP_UNAUTHORIZED)
        r = requests.get('%s/login' % SERVER_URL, params={'password': 'moshe'})
        self.assertEqual(r.status_code, utils.HTTP_UNAUTHORIZED)

    def test_bad_verbs(self):
        r = requests.put('%s/login' % SERVER_URL, params=self.user_and_password)
        self.assertEqual(r.status_code, utils.HTTP_METHOD_NOT_ALLOWED)
        r = requests.delete('%s/login' % SERVER_URL, params=self.user_and_password)
        self.assertEqual(r.status_code, utils.HTTP_METHOD_NOT_ALLOWED)
        r = requests.patch('%s/login' % SERVER_URL, params=self.user_and_password)
        self.assertEqual(r.status_code, utils.HTTP_METHOD_NOT_ALLOWED)
