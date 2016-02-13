import json
import unittest

import mock as mock
import requests
from org.gi.server.server import app

from misc import _remove_from_db, _push_to_db, MONGO, SERVER_URL, _load
import org.gi.server.authorization as auth
import org.gi.server.utils as util
from org.gi.server.web_token import get_user_from_access_token

FB_TOKEN = 'we_mock_responses_anyway'


class GIFacebookLoginAndUserCreationTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GIFacebookLoginAndUserCreationTests, self).__init__(*args, **kwargs)
        self.config_folder = 'facebook'
        app.config['SECRET_KEY'] = 'JA_SECRET!'
        self.app = app.test_client()

    def setUp(self):
        _remove_from_db(MONGO, 'users')

    def tearDown(self):
        _remove_from_db(MONGO, 'users')

    # negatives

    def test_no_token(self):
        r = requests.get('{}/login/fb_token/'.format(SERVER_URL))
        self.assertEqual(r.status_code, 404)

    def test_bad_http_methods(self):
        r = requests.post('{}/login/fb_token/{}'.format(SERVER_URL, FB_TOKEN))
        self.assertEqual(r.status_code, 405)
        r = requests.put('{}/login/fb_token/{}'.format(SERVER_URL, FB_TOKEN))
        self.assertEqual(r.status_code, 405)
        r = requests.delete('{}/login/fb_token/{}'.format(SERVER_URL, FB_TOKEN))
        self.assertEqual(r.status_code, 405)
        r = requests.patch('{}/login/fb_token/{}'.format(SERVER_URL, FB_TOKEN))
        self.assertEqual(r.status_code, 405)

    @mock.patch('org.gi.server.facebook.facebook')
    def test_fb_no_response(self, fb_mock):
        fb_mock.get.return_value = util.Map({
            'status': util.HTTP_SERVICE_UNAVAILABLE,
            'data': {'error': {'message': 'Mock error'}}
        })
        resp = self.app.get('/login/fb_token/{}'.format(FB_TOKEN))
        self.assertEqual('Mock error', resp.data)
        self.assertEqual(util.HTTP_SERVICE_UNAVAILABLE, resp.status_code)

    @mock.patch('org.gi.server.facebook.facebook')
    def test_fb_response_missing_required_info(self, fb_mock):
        users_missing_info = _load('fb_users_missing_required_fields.json', self.config_folder)
        for user_missing_info in users_missing_info:
            fb_mock.get.return_value = util.Map({
                'status': util.HTTP_OK,
                'data': user_missing_info
            })
            resp = self.app.get('/login/fb_token/{}'.format(FB_TOKEN))
            self.assertEqual(util.HTTP_BAD_INPUT, resp.status_code)
            faults = json.loads(resp.data)
            self.assertTrue(isinstance(faults, list))
            self.assertTrue(len(faults) > 0)

    @mock.patch('org.gi.server.facebook.facebook')
    def test_fb_user_fails_to_validate(self, fb_mock):
        users_with_invalid_data = _load('fb_users_with_invalid_data.json', self.config_folder)
        for user_with_invalid_data in users_with_invalid_data:
            fb_mock.get.return_value = util.Map({
                'status': util.HTTP_OK,
                'data': user_with_invalid_data
            })
            resp = self.app.get('/login/fb_token/{}'.format(FB_TOKEN))
            self.assertEqual(util.HTTP_BAD_INPUT, resp.status_code)
            faults = json.loads(resp.data)
            self.assertTrue(isinstance(faults, list))
            self.assertTrue(len(faults) > 0)

    @mock.patch('org.gi.server.facebook.facebook')
    def test_user_exists_without_fb_id(self, fb_mock):
        inserted_user = _load('a_user.json', self.config_folder)
        inserted_user['password'] = auth.hash_password(inserted_user['password'])
        _push_to_db(MONGO, 'users', [inserted_user])

        clashing_fb_user = _load('clashing_fb_user.json', self.config_folder)
        fb_mock.get.return_value = util.Map({
            'status': util.HTTP_OK,
            'data': clashing_fb_user
        })

        resp = self.app.get('/login/fb_token/{}'.format(FB_TOKEN))
        self.assertEqual(util.HTTP_BAD_INPUT, resp.status_code)
        self.assertTrue('already exists' in resp.data)
        self.assertTrue(clashing_fb_user['email'] in resp.data)

    # positives

    @mock.patch('org.gi.server.facebook.facebook')
    def test_user_created_successfully(self, fb_mock):
        good_user = _load('a_fb_user.json', self.config_folder)
        fb_mock.get.return_value = util.Map({
            'status': util.HTTP_OK,
            'data': good_user
        })

        resp = self.app.get('/login/fb_token/{}'.format(FB_TOKEN))
        self.assertEqual(util.HTTP_OK, resp.status_code)
        self.assertTrue(isinstance(get_user_from_access_token(resp.data), dict))

    @mock.patch('org.gi.server.facebook.facebook')
    def test_user_already_exists(self, fb_mock):
        existing_user = _load('existing_fb_user.json', self.config_folder)
        fb_mock.get.return_value = util.Map({
            'status': util.HTTP_OK,
            'data': existing_user
        })

        resp = self.app.get('/login/fb_token/{}'.format(FB_TOKEN))
        self.assertEqual(util.HTTP_OK, resp.status_code)
        self.assertTrue(isinstance(get_user_from_access_token(resp.data), dict))

        # User already exists!
        resp = self.app.get('/login/fb_token/{}'.format(FB_TOKEN))
        self.assertEqual(util.HTTP_OK, resp.status_code)
        self.assertTrue(isinstance(get_user_from_access_token(resp.data), dict))

    @mock.patch('org.gi.server.facebook.facebook')
    def test_create_many_users(self, fb_mock):
        fb_users = _load('fb_users.json', self.config_folder)

        for fb_user in fb_users:
            fb_mock.get.return_value = util.Map({
                'status': util.HTTP_OK,
                'data': fb_user
            })

            resp = self.app.get('/login/fb_token/{}'.format(FB_TOKEN))
            self.assertEqual(util.HTTP_OK, resp.status_code)
            self.assertTrue(isinstance(get_user_from_access_token(resp.data), dict))









