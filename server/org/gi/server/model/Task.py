from org.gi.server.validation.task_state_machine import TASK_PENDING_USER_APPROVAL, TASK_ASSIGNMENT_IN_PROCESS
from org.gi.server.validation.case_state_machine import CASE_ASSIGNED, \
    CASE_PENDING_INVOLVEMENT, CASE_COMPLETED, CASE_PARTIALLY_ASSIGNED, CASE_PARTIALLY_COMPLETED
from org.gi.server.validation.task_state_machine import TASK_PENDING, TASK_ASSIGNED, TASK_COMPLETED

ALL_TASKS_SAME_STATE_TRANSITION = {
    TASK_PENDING: CASE_PENDING_INVOLVEMENT,
    TASK_ASSIGNED: CASE_ASSIGNED,
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
            if {TASK_COMPLETED, TASK_ASSIGNED}.issubset(task_states):
                updated_case_state = CASE_PARTIALLY_COMPLETED

        if not updated_case_state:
            raise BadTaskStateException('A case cannot have the following states together {}'.format(task_states))

        return updated_case_state

    @staticmethod
    def merge_non_updated_tasks(updated_tasks, existing_tasks):
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


class BadTaskStateException(Exception):
    pass
