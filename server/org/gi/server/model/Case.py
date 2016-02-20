import uuid

from org.gi.server.model.task import Task
from org.gi.server import location as l
from org.gi.server.validation.case_state_machine import CASE_UNDEFINED, CASE_PENDING_APPROVAL, CASE_MISSING_INFO, \
    CASE_REJECTED, CASE_OVERDUE, CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN
from org.gi.server.validation.task_state_machine import TASK_PENDING


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
        Case.handle_geo_location(updated_case)
        return updated_case

    @staticmethod
    def handle_geo_location(case):
        if 'tasks' not in case:
            return
        fields = ['destination_address', 'address']
        for task in case['tasks']:
            for field in fields:
                address = task.get(field)
                if address:
                    geo = l.get_lat_lng(address)
                    address['geo'] = geo

    @staticmethod
    def prep_case_before_insert(case):
        if 'state' not in case or case['state'] == CASE_UNDEFINED:
            case['state'] = CASE_PENDING_APPROVAL
        for task in case['tasks']:
            task['id'] = str(uuid.uuid4())
            task['state'] = TASK_PENDING
        Case.handle_geo_location(case)
        return case