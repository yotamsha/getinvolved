import unittest

from misc import _remove_from_db, _load, _push_to_db, MONGO, SERVER_URL, validate_server_is_up
import org.gi.server.authorization as auth
import requests
from requests.auth import HTTPBasicAuth


class GIAccessTokenAuthentication(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIAccessTokenAuthentication, self).__init__(*args, **kwargs)
        self.config_folder = 'auth'
        self._user = _load('user.json', self.config_folder)
        self._auth = HTTPBasicAuth(self._user['user_name'], self._user['password'])

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

    def test_user_login(self):
        r = requests.get('%s/login' % SERVER_URL, auth=self._auth)
        self.assertEqual(r.status_code, 200)
        r = requests.post('%s/login' % SERVER_URL, auth=self._auth)
        self.assertEqual(r.status_code, 200)

    def test_password_all_caps(self):
        user = self._user.copy()
        _auth = HTTPBasicAuth(user['user_name'], user['password'].upper())
        r = requests.post('%s/login' % SERVER_URL, auth=_auth)
        self.assertEqual(r.status_code, 401)

    def test_user_all_caps(self):
        user = self._user.copy()
        _auth = HTTPBasicAuth(user['user_name'].upper(), user['password'])
        r = requests.post('%s/login' % SERVER_URL, auth=_auth)
        self.assertEqual(r.status_code, 401)

    def test_user_bad_password_login(self):
        user = self._user.copy()
        _auth = HTTPBasicAuth(user['user_name'], user['password'] + '7')
        r = requests.get('%s/login' % SERVER_URL, auth=_auth)
        self.assertEqual(401, r.status_code)

    def test_login_ok_wrong_cred(self):
        _auth = HTTPBasicAuth('admin', 'hamin')
        r = requests.get('%s/login' % SERVER_URL, auth=_auth)
        self.assertEqual(r.status_code, 401)

    def test_bad_header(self):
        r = requests.get('%s/login' % SERVER_URL, headers={'Authorization': 'thisbad'})
        self.assertEqual(r.status_code, 401)

    def test_no_header(self):
        r = requests.get('%s/login' % SERVER_URL)
        self.assertEqual(r.status_code, 401)

    def test_bad_verbs(self):
        r = requests.put('%s/login' % SERVER_URL, auth=self._auth)
        self.assertEqual(r.status_code, 405)
        r = requests.delete('%s/login' % SERVER_URL, auth=self._auth)
        self.assertEqual(r.status_code, 405)
        r = requests.patch('%s/login' % SERVER_URL, auth=self._auth)
        self.assertEqual(r.status_code, 405)
