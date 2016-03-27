import sys

from org.gi.server.validation.case_state_machine import CASE_ASSIGNED, \
    CASE_PENDING_INVOLVEMENT, CASE_COMPLETED, CASE_PARTIALLY_ASSIGNED, CASE_PARTIALLY_COMPLETED
from org.gi.server.validation.task.task_state_machine import TASK_PENDING, TASK_ASSIGNED, TASK_COMPLETED, \
    TASK_ATTENDANCE_CONFIRMED, TASK_UNDEFINED
from org.gi.server.validation.task.task_state_machine import TASK_PENDING_USER_APPROVAL, TASK_ASSIGNMENT_IN_PROCESS

ALL_TASKS_SAME_STATE_TRANSITION = {
    TASK_PENDING: CASE_PENDING_INVOLVEMENT,
    TASK_ASSIGNED: CASE_ASSIGNED,
    TASK_ATTENDANCE_CONFIRMED: CASE_ASSIGNED,
    TASK_COMPLETED: CASE_COMPLETED
}


class Task:
    def __init__(self):
        pass

    @staticmethod
    def get_logical_state(state):
        if state in {TASK_ASSIGNMENT_IN_PROCESS, TASK_PENDING_USER_APPROVAL}:
            state = TASK_PENDING
        return state

    @staticmethod
    def get_updated_case_state(updated_tasks, db_tasks=None):
        updated_case_state = ''
        task_states = set()
        for task in updated_tasks:
            task_state = Task.get_logical_state(task.get('state'))
            if task_state:
                task_states.add(task_state)
        if db_tasks:
            for db_task in db_tasks:
                db_task_is_updated = False
                for task in updated_tasks:
                    if task.get('id') == db_task.get('id'):
                        db_task_is_updated = True
                        break
                if not db_task_is_updated:
                    task_states.add(Task.get_logical_state(db_task.get('state')))

        if len(task_states) == 1:
            updated_case_state = ALL_TASKS_SAME_STATE_TRANSITION.get(task_states.pop())
        elif len(task_states) == 2:
            if {TASK_PENDING, TASK_ASSIGNED}.issubset(task_states):
                updated_case_state = CASE_PARTIALLY_ASSIGNED
            if {TASK_ASSIGNED, TASK_ATTENDANCE_CONFIRMED}.issubset(task_states):
                updated_case_state = CASE_ASSIGNED
            if {TASK_COMPLETED, TASK_ASSIGNED}.issubset(task_states):
                updated_case_state = CASE_PARTIALLY_COMPLETED
            if {TASK_ATTENDANCE_CONFIRMED, TASK_COMPLETED}.issubset(task_states):
                updated_case_state = CASE_PARTIALLY_COMPLETED
        elif len(task_states) == 3:
            if {TASK_ASSIGNED, TASK_ATTENDANCE_CONFIRMED, TASK_COMPLETED}.issubset(task_states):
                updated_case_state = CASE_PARTIALLY_COMPLETED

        if not updated_case_state and task_states:
            raise BadTaskStateException('Cannot have the following TASK states together {}'.format(task_states))

        return updated_case_state

    @staticmethod
    def get_unique_tasks_by_id(updated_tasks, existing_tasks):
        merged_tasks = []
        for existing_task in existing_tasks:
            if not Task.does_task_exist_in_task_list(existing_task, updated_tasks):
                merged_tasks.append(existing_task)
        merged_tasks += updated_tasks
        return merged_tasks

    @staticmethod
    def does_task_exist_in_task_list(task, task_list):
        for db_task in task_list:
            if task.get('id') and db_task.get('id') and task.get('id') == db_task.get('id'):
                return True
        return False

    @classmethod
    def get_nearest_due_date(cls, tasks):
        nearest_due_date = sys.maxint
        if len(tasks) > 1:
            nearest_due_date = tasks[0]['due_date']
        for task in tasks:
            if task.get('due_date') < nearest_due_date:
                nearest_due_date = task.get('due_date')
        return nearest_due_date

    @classmethod
    def update_task_state(cls, task, db_tasks):
        task_state = TASK_PENDING
        if Task.does_task_exist_in_task_list(task, db_tasks):  # task cant be created with volunteer assigned (!)
            if task.get('volunteer_id') and Task.state_before_assigned(task.get('state')):
                task_state = TASK_ASSIGNED
            elif task.get('state'):
                task_state = task.get('state')
        return task_state

    @classmethod
    def state_before_assigned(cls, curr_task_state):
        return curr_task_state and curr_task_state in [TASK_PENDING]


class BadTaskStateException(Exception):
    pass

