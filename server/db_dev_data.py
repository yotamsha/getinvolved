#!/usr/bin/python
import requests
import json
import time

from org.gi import args
from org.gi.server.db import mongo
from org.gi.server.utils import get_hours_in_seconds
from org.gi.server.validation.task.task_state_machine import TASK_ASSIGNED
from org.gi.server.web_token import AccessTokenAuth

SERVER_URL = 'http://localhost:5000'
SERVER_URL_API = 'http://localhost:5000/api'


def next_due_date():
    next_due_date.counter += 1
    return int(time.time()) + get_hours_in_seconds(24 + next_due_date.counter)


next_due_date.counter = 0


def load_db():
    global access_token
    users_endpoint = '%s/users' % SERVER_URL_API
    with open("dev_data/first_user.json") as _user:
        user = json.load(_user)
        r = requests.post(users_endpoint, json=user)
        user_credentials = {
            'username': user['user_name'],
            'password': user['password']
        }
        r = requests.get('%s/login' % SERVER_URL, params=user_credentials)
        access_token = AccessTokenAuth(r.content)

    petitioner_ids = []
    with open("dev_data/petitioners.json", "r") as _users:
        users = json.load(_users)
        insert_entities(users_endpoint, petitioner_ids, users)

    case_ids = []
    with open("dev_data/cases.json", "r") as _cases:
        cases = json.load(_cases)
        cases_endpoint = '%s/cases' % SERVER_URL_API
        for user_id, case in zip(petitioner_ids, cases):
            case['petitioner_id'] = user_id
        for case in cases:
            for task in case['tasks']:
                task['due_date'] = next_due_date()
        insert_entities(cases_endpoint, case_ids, cases)

    volunteer_ids = []
    with open("dev_data/volunteers.json", "r") as _users:
        users = json.load(_users)
        users_endpoint = '%s/users' % SERVER_URL_API
        insert_entities(users_endpoint, volunteer_ids, users)

    for index in range(len(case_ids) - 1):
        r = requests.get(cases_endpoint + "/{}".format(case_ids[index]), auth=access_token)
        case = json.loads(r.content)
        for volunteer_id, task in zip(volunteer_ids, case['tasks']):
            task['volunteer_id'] = volunteer_id
            task['state'] = TASK_ASSIGNED
        requests.put(cases_endpoint + "/{}".format(case_ids[index]), auth=access_token, json=case)


def insert_entities(endpoint, entity_ids, entities):
    for entity in entities:
        r = requests.post(endpoint, auth=access_token, json=entity)
        print "{} {}".format(r.content, r.status_code)
        if r.status_code == 201:
            json_user = json.loads(r.content)
            entity_ids.append(json_user['id'])


def clear_database():
    db = mongo.get_default_database()
    db['users'].delete_many({})
    db['cases'].delete_many({})


if __name__ == "__main__":
    clear_db = args.clear
    if clear_db:
        clear_database()
    else:
        load_db()
