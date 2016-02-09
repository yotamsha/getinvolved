import unittest
from misc import _remove_from_db, _load, _push_to_db, MONGO, SERVER_URL
import org.gi.server.authorization as auth
import requests
from requests.auth import HTTPBasicAuth


class GIAccessTokenAuthentication(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIAccessTokenAuthentication, self).__init__(*args, **kwargs)
        self.config_folder = 'auth'
        self.user = _load('user.json', self.config_folder)
        self.access_token = u""

    def setUp(self):
        _remove_from_db(MONGO, 'users')
        user = self.user
        user['password'] = auth.hash_password(user['password'])
        self.id = _push_to_db(MONGO, 'users', [user])

    def tearDown(self):
        _remove_from_db(MONGO, 'users')

    def test_user_login(self):
        _auth = HTTPBasicAuth(self.user['user_name'], self.user['password'])
        r = requests.get('%s/login' % SERVER_URL, auth=_auth)
        self.access_token = r.content
        self.assertEqual(200, r.status_code)

    def test_access_token(self):
        # user = _load('user.json', self.config_folder)
        # _auth = HTTPBasicAuth(user['user_name'], user['password'])
        # r = requests.get('%s/login' % SERVER_URL, auth=_auth)
        path = '%s/test_access_token' % API_SERVER_URL
        # access_token = r.content
        access_token = "LALALA"
        r = requests.get(path, auth=access_token)
        print r.content
        self.assertEqual(200, r.status_code)