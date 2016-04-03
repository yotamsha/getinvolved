import unittest

from org.gi.server.model.Case import Case
from org.gi.server.validation.case_state_machine import CASE_UNDEFINED, CASE_PENDING_APPROVAL, CASE_MISSING_INFO, \
    CASE_REJECTED, CASE_OVERDUE, CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN, CASE_PENDING_INVOLVEMENT, \
    CASE_PARTIALLY_ASSIGNED, CASE_ASSIGNED, CASE_PARTIALLY_COMPLETED, CASE_COMPLETED


class TestCaseModel(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCaseModel, self).__init__(*args, **kwargs)

    # positives

    def test_case_due_date_set(self):
        case = {
            'tasks': [
                {'due_date': 700},
                {'due_date': 300},
                {'due_date': 200}
            ]
        }
        Case.prep_case_before_insert(case)
        self.assertEqual(200, case['due_date'])

    def test_case_due_date_updated(self):
        updated_case = {
            'tasks': [
                {
                    'id': 1,
                    'due_date': 700
                },
                {
                    'id': 2,
                    'due_date': 300
                }
            ]
        }
        db_case = {
            'tasks': [
                {
                    'id': 1,
                    'due_date': 100
                },
                {
                    'id': 2,
                    'due_date': 300
                }
            ]
        }
        Case.prep_case_before_update(updated_case, db_case)
        self.assertEqual(300, updated_case['due_date'])

    def test_case_state_update_override(self):
        self.assertTrue(Case._changeless_state(CASE_MISSING_INFO))
        self.assertTrue(Case._changeless_state(CASE_REJECTED))
        self.assertTrue(Case._changeless_state(CASE_OVERDUE))
        self.assertTrue(Case._changeless_state(CASE_CANCELLED_BY_USER))
        self.assertTrue(Case._changeless_state(CASE_CANCELLED_BY_ADMIN))

    # negatives

    def test_case_state_update_not_override(self):
        self.assertFalse(Case._changeless_state(CASE_UNDEFINED))
        self.assertFalse(Case._changeless_state(CASE_PENDING_APPROVAL))
        self.assertFalse(Case._changeless_state(CASE_PENDING_INVOLVEMENT))
        self.assertFalse(Case._changeless_state(CASE_PARTIALLY_ASSIGNED))
        self.assertFalse(Case._changeless_state(CASE_ASSIGNED))
        self.assertFalse(Case._changeless_state(CASE_PARTIALLY_COMPLETED))
        self.assertFalse(Case._changeless_state(CASE_COMPLETED))
