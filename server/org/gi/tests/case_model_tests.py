import unittest

from org.gi.server.model.Case import Case
from org.gi.server.validation.case_state_machine import CASE_UNDEFINED, CASE_PENDING_APPROVAL, CASE_MISSING_INFO, \
    CASE_REJECTED, CASE_OVERDUE, CASE_CANCELLED_BY_USER, CASE_CANCELLED_BY_ADMIN, CASE_PENDING_INVOLVEMENT, \
    CASE_PARTIALLY_ASSIGNED, CASE_ASSIGNED, CASE_PARTIALLY_COMPLETED, CASE_COMPLETED


class TestCaseModel(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCaseModel, self).__init__(*args, **kwargs)

    # positives

    def test_case_state_update_override(self):
        self.assertTrue(Case._update_state_overrides_transition(CASE_MISSING_INFO))
        self.assertTrue(Case._update_state_overrides_transition(CASE_REJECTED))
        self.assertTrue(Case._update_state_overrides_transition(CASE_OVERDUE))
        self.assertTrue(Case._update_state_overrides_transition(CASE_CANCELLED_BY_USER))
        self.assertTrue(Case._update_state_overrides_transition(CASE_CANCELLED_BY_ADMIN))

    # negatives

    def test_case_state_update_not_override(self):
        self.assertFalse(Case._update_state_overrides_transition(CASE_UNDEFINED))
        self.assertFalse(Case._update_state_overrides_transition(CASE_PENDING_APPROVAL))
        self.assertFalse(Case._update_state_overrides_transition(CASE_PENDING_INVOLVEMENT))
        self.assertFalse(Case._update_state_overrides_transition(CASE_PARTIALLY_ASSIGNED))
        self.assertFalse(Case._update_state_overrides_transition(CASE_ASSIGNED))
        self.assertFalse(Case._update_state_overrides_transition(CASE_PARTIALLY_COMPLETED))
        self.assertFalse(Case._update_state_overrides_transition(CASE_COMPLETED))

