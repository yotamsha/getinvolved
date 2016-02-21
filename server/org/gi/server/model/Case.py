import uuid

from org.gi.server.model.Task import Task
from org.gi.server.service import location as l
from org.gi.server.validation.case_state_machine import CASE_UNDEFINED, CASE_PENDING_APPROVAL, CASE_MISSING_INFO, \
    CASE_REJECTED, CASE_OVERDUE, CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN
from org.gi.server.validation.task.task_state_machine import TASK_PENDING


class Case:
    def __init__(self):
        pass

    @staticmethod
    def _update_state_overrides_transition(update_state):
        override = False
        if update_state in {CASE_MISSING_INFO, CASE_REJECTED, CASE_OVERDUE,
                            CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN}:
            override = True
        return override

    @staticmethod
    def prep_case_before_update(updated_case, db_case):
        if not Case._update_state_overrides_transition(updated_case.get('state')) and updated_case.get('tasks'):
            updated_case['state'] = Task.get_updated_case_state(updated_case.get('tasks'), db_case.get('tasks'))

        if updated_case.get('tasks'):
            updated_case['tasks'] = Task.merge_non_updated_tasks(updated_case.get('tasks'), db_case.get('tasks'))
            for task in updated_case['tasks']:
                if not task.get('id'):
                    task['id'] = str(uuid.uuid4())

        # We add this param.
        if 'id' in updated_case:
            del updated_case['id']

        Case.handle_geo_location(updated_case)
        return updated_case

    @staticmethod
    def prep_case_before_insert(case):
        if 'state' not in case or case['state'] == CASE_UNDEFINED:
            case['state'] = CASE_PENDING_APPROVAL
        for task in case['tasks']:
            task['id'] = str(uuid.uuid4())
            task['state'] = TASK_PENDING
        Case.handle_geo_location(case)
        return case

    @staticmethod
    def handle_geo_location(case):
        if case.get('location'):
            _retrieve_all_location_data(case.get('location'))
        if 'tasks' not in case:
            return
        fields = ['destination', 'location']
        for task in case['tasks']:
            for field in fields:
                location = task.get(field)
                if location:
                    _retrieve_all_location_data(location)


def _retrieve_all_location_data(location):
    if location.get('address'):
        geo = l.get_lat_lng(location.get('address'))
        location['geo_location'] = geo
    elif location.get('geo_location'):
        geo = location.get('geo_location')
        address = l.get_address(geo.get('lat'), geo.get('lng'))
        location['address'] = address
