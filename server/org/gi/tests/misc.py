import time

from org.gi.server.service.notification.notification import SECONDS_IN_HOUR

__author__ = 'avishayb'

from org.gi.config import config
import pymongo
import requests
import sys
import json
import os
from os import listdir
from os.path import isfile, join
from org.gi.server.web_token import generate_access_token, AccessTokenAuth
import org.gi.server.utils as utils

from requests.exceptions import ConnectionError

DB_URI = config.get_db_uri()
SERVER_URL = 'http://localhost:5000'
SERVER_URL_API = 'http://localhost:5000/api'
MONGO = pymongo.MongoClient(DB_URI)

SERVER_DOWN_MSG = 'No response from GI Server (%s). Make sure its up and running.'
SERVER_NO_PING = 'Bad response (%d) from Ping call. Try HTTP GET to %s'


def validate_server_is_up():
    try:
        ping_url = '%s/ping' % SERVER_URL_API
        r = requests.get(ping_url)
        if r.status_code != utils.HTTP_OK:
            raise Exception(SERVER_NO_PING % (r.status_code, ping_url))
    except ConnectionError as ce:
        raise Exception (SERVER_DOWN_MSG % str(ce))


def _get_id(self):
    _push_to_db(MONGO, 'users', self.users)
    r = requests.get('%s/users' % SERVER_URL_API)
    self.assertEqual(r.status_code, utils.HTTP_OK)
    return r.json()['users'][0]['id']


def _load(file_name, folder_name):
    path = sys.modules[__name__].__file__
    path = path[:path.rfind(os.path.sep)]
    with open('%s/config/%s/%s' % (path, folder_name, file_name)) as data_file:
        return json.load(data_file)

def _load_binary(file_name, folder_name):
    path = sys.modules[__name__].__file__
    path = path[:path.rfind(os.path.sep)]
    with open('%s/config/%s/%s' % (path, folder_name, file_name),mode='rb') as file:
        return file.read()

def list_files(folder_name):
    path = sys.modules[__name__].__file__
    path = path[:path.rfind(os.path.sep)] + '/config/' + folder_name
    return [f for f in listdir(path) if isfile(join(path, f))]

ACCESS_TOKEN_AUTH = AccessTokenAuth(generate_access_token(_load('fake_db_user.json', 'auth')))


def _push_to_db(mongo, collection_name, data):
    if not isinstance(data, list):
        data = [data]
    db = mongo.get_default_database()
    db[collection_name].insert_many(data)
    return _get_ids(mongo, collection_name)


def _remove_from_db(mongo, collection_name):
    db = mongo.get_default_database()
    db[collection_name].delete_many({})


def _get_ids(mongo, collection_name):
    db = mongo.get_default_database()
    records = db[collection_name].find()
    return [str(r['_id']) for r in records]


def _get_legal_due_date():
    return int(time.time()) + SECONDS_IN_HOUR * 25
