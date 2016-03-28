#!/usr/bin/python
import getopt

import requests
import json
import time
import argparse

import sys

from org.gi import args
from org.gi.server.db import mongo
from org.gi.server.utils import get_hours_in_seconds
from org.gi.server.validation.task.task_state_machine import TASK_ASSIGNED
from org.gi.tests.misc import ACCESS_TOKEN_AUTH, SERVER_URL_API

access_token = ACCESS_TOKEN_AUTH


def next_due_date():
    next_due_date.counter += 1
    return int(time.time()) + get_hours_in_seconds(24 + next_due_date.counter)


next_due_date.counter = 0


def load_db():
    petitioner_ids = []
    with open("dev_data/petitioners.json", "r") as _users:
        users = json.load(_users)
        users_endpoint = '%s/users' % SERVER_URL_API
        insert_entities(users_endpoint, petitioner_ids, users)

    case_ids = []
    with open("dev_data/cases.json", "r") as _cases:
        cases = json.load(_cases)
        cases_endpoint = '%s/cases' % SERVER_URL_API
        for user_id, case in zip(petitioner_ids, cases):
            case['petitioner_id'] = user_id
            for task in case['tasks']:
                task['due_date'] = next_due_date()
        insert_entities(cases_endpoint, case_ids, cases)

    volunteer_ids = []
    with open("dev_data/volunteers.json", "r") as _users:
        users = json.load(_users)
        users_endpoint = '%s/users' % SERVER_URL_API
        insert_entities(users_endpoint, volunteer_ids, users)

    for index in range(len(case_ids) - 1):
        r = requests.get(cases_endpoint + "/{}".format(case_ids[index]), auth=ACCESS_TOKEN_AUTH)
        case = json.loads(r.content)
        for volunteer_id, task in zip(volunteer_ids, case['tasks']):
            task['volunteer_id'] = volunteer_id
            task['state'] = TASK_ASSIGNED
        requests.put(cases_endpoint + "/{}".format(case_ids[index]), auth=ACCESS_TOKEN_AUTH, json=case)


def insert_entities(endpoint, entity_ids, entities):
    for entity in entities:
        r = requests.post(endpoint, auth=ACCESS_TOKEN_AUTH, json=entity)
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
