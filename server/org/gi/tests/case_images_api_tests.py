import unittest
import requests
import org.gi.server.utils as utils
from misc import _remove_from_db, _push_to_db, MONGO, SERVER_URL_API, ACCESS_TOKEN_AUTH, _load_binary, _load, \
    validate_server_is_up, list_files

from org.gi.tests.users_tests import CONFIG_DATA_DIRECTORY as USER_CONFIG_DATA_DIRECTORY
from org.gi.tests.cases_tests import CONFIG_DATA_DIRECTORY as CASE_CONFIG_DATA_DIRECTORY


CONFIG_DATA_DIRECTORY = 'case_images'


class TestCaseImagesAPIl(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCaseImagesAPIl, self).__init__(*args, **kwargs)
        self.users = _load('users.json', USER_CONFIG_DATA_DIRECTORY)
        self.cases = _load('cases.json', CASE_CONFIG_DATA_DIRECTORY)

    @classmethod
    def setUpClass(cls):
        validate_server_is_up()

    def setUp(self):
        _remove_from_db(MONGO, 'users')
        _remove_from_db(MONGO, 'cases')
        self.user_ids = _push_to_db(MONGO, 'users', self.users)
        self.case_ids = _push_to_db(MONGO, 'cases', self.cases)

    def tearDown(self):
        _remove_from_db(MONGO, 'users')
        _remove_from_db(MONGO, 'cases')

    def test_upload_and_delete(self):
        files = list_files(CONFIG_DATA_DIRECTORY)
        files_to_delete = []
        for f in files:
            image = _load_binary(f, CONFIG_DATA_DIRECTORY)
            files = {'file': image}
            r = requests.post('%s/cases/%s/images?file_name=%s' % (SERVER_URL_API, self.case_ids[0], f),
                              auth=ACCESS_TOKEN_AUTH, files=files)
            self.assertEqual(r.status_code, utils.HTTP_CREATED, msg=r.text)
            files_to_delete.append(r.json()['image_url'].split('/')[-1])
        for f in files_to_delete:
            r = requests.delete('%s/cases/%s/images/%s' % (SERVER_URL_API, self.case_ids[0], f), auth=ACCESS_TOKEN_AUTH)
            self.assertEqual(r.status_code, utils.HTTP_NO_CONTENT, msg=r.text)




