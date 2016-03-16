import uuid
import time

from org.gi.server.model.Location import Location
from org.gi.server.model.Task import Task
from org.gi.server import utils as utils
from org.gi.server.validation.case_state_machine import CASE_UNDEFINED, CASE_PENDING_APPROVAL, CASE_MISSING_INFO, \
    CASE_REJECTED, CASE_OVERDUE, CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN
from org.gi.server.validation.task.task_state_machine import TASK_PENDING
from org.gi.server import utils as u
from org.gi.server.db import db


class Case:
    def __init__(self):
        pass

    @staticmethod
    def prep_case_before_insert(case):
        if 'state' not in case or case['state'] == CASE_UNDEFINED:
            case['state'] = CASE_PENDING_APPROVAL
        for task in case['tasks']:
            task['id'] = str(uuid.uuid4())
            task['state'] = TASK_PENDING
        case['due_date'] = Task.get_nearest_due_date(case.get('tasks'))
        case['creation_date'] = int(time.time())
        Case.handle_geo_location(case)
        return case

    @staticmethod
    def prep_case_before_update(updated_case, db_case):
        if not Case._update_state_overrides_transition(updated_case.get('state')) and updated_case.get('tasks'):
            updated_case['state'] = Task.get_updated_case_state(updated_case.get('tasks'), db_case.get('tasks'))

        if updated_case.get('tasks'):
            for task in updated_case['tasks']:
                if not task.get('id'):
                    task['id'] = str(uuid.uuid4())

            updated_case['tasks'] = Task.get_unique_tasks_by_id(updated_case.get('tasks'), db_case.get('tasks'))
            updated_case['due_date'] = Task.get_nearest_due_date(updated_case['tasks'])

        # 'id' is duplicate of mongo '_id', don't want to store it
        if 'id' in updated_case:
            del updated_case['id']

        Case.handle_geo_location(updated_case)
        return updated_case

    @staticmethod
    def _update_state_overrides_transition(update_state):
        override = False
        if update_state in {CASE_MISSING_INFO, CASE_REJECTED, CASE_OVERDUE,
                            CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN}:
            override = True
        return override


    @staticmethod
    def handle_geo_location(case):
        if case.get('location'):
            Location.retrieve_all_location_data(case.get('location'))
            Location.change_geo_location_to_db_format(case.get('location'))
        if 'tasks' not in case:
            return
        fields = ['destination', 'location']
        for task in case['tasks']:
            for field in fields:
                location = task.get(field)
                if location:
                    Location.retrieve_all_location_data(location)
                    Location.change_geo_location_to_db_format(location)

    @classmethod
    def prep_case_for_client(cls, case, add_volunteer_attributes=False):
        utils.handle_id(case)
        Location.change_geo_location_to_client_format(case.get('location'))
        for task in case.get('tasks'):
            Location.change_geo_location_to_client_format(task.get('location'))
            if add_volunteer_attributes and task['volunteer_id']:
                volunteer_id = task['volunteer_id']
                user = db.users.find_one({'_id': u.to_object_id(volunteer_id)})
                u.handle_id(user)
                task['volunteer'] = user




