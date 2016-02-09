__author__ = 'avishayb'
import unittest
import requests
from misc import SERVER_URL

class GILoginTestCase(unittest.TestCase):
    def test_login_ok_wrong_cred(self):
        r = requests.get('%s/login?user_name=jack&password=secret' % SERVER_URL)
        self.assertEqual(r.status_code, 401)

    def test_login_ok_good_cred(self):
        r = requests.get('%s/login?user_name=admin&password=admin' % SERVER_URL)
        self.assertEqual(r.status_code, 200)

    def test_login_no_password(self):
        r = requests.get('%s/login?user_name=admin&password___=admin' % SERVER_URL)
        self.assertEqual(r.status_code, 400)

    def test_login_no_user(self):
        r = requests.get('%s/login?user_name___=admin&password=admin' % SERVER_URL)
        self.assertEqual(r.status_code, 400)

