import unittest

from org.gi.server.model.task import Task, BadTaskStateException
from org.gi.server.validation.case_state_machine import CASE_UNDEFINED, CASE_PENDING_INVOLVEMENT, \
    CASE_PARTIALLY_ASSIGNED, CASE_ASSIGNED, CASE_PARTIALLY_COMPLETED, CASE_COMPLETED
from org.gi.server.validation.task_state_machine import TASK_PENDING, TASK_ASSIGNMENT_IN_PROCESS, \
    TASK_PENDING_USER_APPROVAL, TASK_ASSIGNED, TASK_CANCELLED, TASK_COMPLETED
from org.gi.tests.misc import _load


class TestTaskModel(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTaskModel, self).__init__(*args, **kwargs)
        self.config_folder = 'task_model'

    # positives

    def test_logical_state(self):
        self.assertEqual(TASK_PENDING, Task.get_logical_state(TASK_ASSIGNMENT_IN_PROCESS))
        self.assertEqual(TASK_PENDING, Task.get_logical_state(TASK_PENDING_USER_APPROVAL))

    def test_logical_state_no_change(self):
        self.assertEqual(TASK_PENDING, Task.get_logical_state(TASK_PENDING))
        self.assertEqual(TASK_ASSIGNED, Task.get_logical_state(TASK_ASSIGNED))
        self.assertEqual(TASK_CANCELLED, Task.get_logical_state(TASK_CANCELLED))
        self.assertEqual(TASK_COMPLETED, Task.get_logical_state(TASK_COMPLETED))
        self.assertTrue(not Task.get_logical_state(None))

    def test_get_updated_case_state(self):
        tasks_pending = _load('tasks_pending.json', self.config_folder)
        self.assertEqual(CASE_PENDING_INVOLVEMENT, Task.get_updated_case_state(tasks_pending, [{'state': TASK_PENDING}]))

        tasks_partially_assigned = _load('tasks_partially_assigned.json', self.config_folder)
        self.assertEqual(CASE_PARTIALLY_ASSIGNED, Task.get_updated_case_state(tasks_partially_assigned),
                         [{'state': TASK_PENDING}, {'state': TASK_ASSIGNMENT_IN_PROCESS}])

        tasks_assigned = _load('tasks_assigned.json', self.config_folder)
        self.assertEqual(CASE_ASSIGNED, Task.get_updated_case_state(tasks_assigned), [{'state': TASK_ASSIGNED}])

        tasks_partially_completed = _load('tasks_partially_completed.json', self.config_folder)
        self.assertEqual(CASE_PARTIALLY_COMPLETED, Task.get_updated_case_state(tasks_partially_completed,
                        [{'state': TASK_ASSIGNED}, {'state': TASK_COMPLETED}]))

        tasks_completed = _load('tasks_completed.json', self.config_folder)
        self.assertEqual(CASE_COMPLETED, Task.get_updated_case_state(tasks_completed), [{'state': TASK_COMPLETED}])

        tasks = [{'state': TASK_COMPLETED, 'id': 0}, {'state': TASK_ASSIGNED, 'id': 1}]
        self.assertEqual(CASE_PARTIALLY_COMPLETED,
                         Task.get_updated_case_state(tasks,
                                                     db_tasks=[
                                                         {'state': TASK_COMPLETED},
                                                         {'state': TASK_CANCELLED, 'id': 0}
                                                     ]))

    # negatives

    def test_bad_state_exception(self):
        tasks_bad_state = _load('tasks_bad_state.json', self.config_folder)
        self.assertRaises(BadTaskStateException, Task.get_updated_case_state, tasks_bad_state)

        tasks_pending = _load('tasks_pending.json', self.config_folder)
        self.assertRaises(BadTaskStateException, Task.get_updated_case_state, tasks_pending,
                        [{'state': TASK_COMPLETED, 'id': 0}, {'state': TASK_CANCELLED, 'id': 1}])

        tasks_partially_assigned = _load('tasks_partially_assigned.json', self.config_folder)
        self.assertRaises(BadTaskStateException, Task.get_updated_case_state, tasks_partially_assigned,
                        [{'state': TASK_COMPLETED, 'id': 0}])

        tasks_partially_completed = _load('tasks_partially_completed.json', self.config_folder)
        self.assertRaises(BadTaskStateException, Task.get_updated_case_state, tasks_partially_completed,
                        [{'state': TASK_PENDING, 'id': 0}])

    def test_merge_task_lists(self):
        partial_list = [{'id': 2}, {'id': 3}]
        orig_list = [{'id': 1}, {'id': 2}]

        merged_list = Task.merge_non_updated_tasks(partial_list, orig_list)
        self.assertEqual(3, len(merged_list))


