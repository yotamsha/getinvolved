__author__ = 'avishayb'

from org.gi.config import config
import pymongo
import requests
import sys
import json
import os
from org.gi.server.web_token import generate_access_token, AccessTokenAuth

DB_URI = config.get_db_uri()
SERVER_URL = 'http://localhost:5000/api'
MONGO = pymongo.MongoClient(DB_URI)


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

AUTH = AccessTokenAuth(generate_access_token(_load('fake_db_user.json', 'auth')))


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

