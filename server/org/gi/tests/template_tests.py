# coding=utf-8
import unittest

from org.gi.server.service.templates.templates import merge, load_and_merge
from org.gi.tests.misc import _load


class GITemplateTestCase(unittest.TestCase):
    # positives

    def test_merge(self):
        self.assertEqual(merge('Hello {{name}}', {'name': 'jack'}), 'Hello jack')

    def test_load_and_merge(self):
        self.assertEqual(load_and_merge('test_only.jinja', {'name': 'jack'}), 'Hello jack')

    def test_merge_list(self):
        self.assertEqual(load_and_merge('/test/test_list.jinja', {'a_list': ['a', 'b', 'c']}), 'abc')

    def test_merge_dict_inner_value(self):
        self.assertEqual(load_and_merge('/test/test_dict.jinja', {'how': {'bout': {'this': 'it works!'}}}), 'it works!')

    def test_load_and_merge_from_directory(self):
        self.assertEqual(load_and_merge('/test/test_only.jinja', {'test': 'success'}), 'Hello success')

    # This method is used to manually verify template correctness,
    # creating the expected results is tedious work
    # AND message templates are subject to change, postponing this for now
    def print_merged_templates(self):
        print "EMAILS:"

        print "Petitioner (NINA):"
        print '###############################################################################'
        all_data = _load('real_world_single_volunteer.json', 'template')
        print load_and_merge('/petitioner/email/first_reminder', all_data['data'], lang='he')
        print '###############################################################################'
        print load_and_merge('/petitioner/email/second_reminder', all_data['data'], lang='he')
        print '###############################################################################'
        print load_and_merge('/petitioner/email/match', all_data['data'], lang='he')
        print '###############################################################################'
        print load_and_merge('/petitioner/email/case_approval', all_data['data'], lang='he')
        print '###############################################################################'

        print "Volunteer (VIKTOR):"
        print '###############################################################################'
        all_data = _load('real_world_volunteer.json', 'template')
        print load_and_merge('/volunteer/email/first_reminder', all_data['data'], lang='he')
        print '###############################################################################'
        print load_and_merge('/volunteer/email/second_reminder', all_data['data'], lang='he')
        print '###############################################################################'
        print load_and_merge('/volunteer/email/register_to_case', all_data['data'], lang='he')
        print '###############################################################################'
        all_data = _load('real_world_volunteer_two.json', 'template')
        print load_and_merge('/volunteer/email/first_reminder', all_data['data'], lang='he')
        print '###############################################################################'
        all_data = _load('real_world_volunteer_three.json', 'template')
        print load_and_merge('/volunteer/email/first_reminder', all_data['data'], lang='he')
        print '###############################################################################'
        print '###############################################################################'
        print '###############################################################################'

        print "SMS:"

        print "Petitioner (NINA):"
        print '###############################################################################'
        all_data = _load('real_world_single_volunteer.json', 'template')
        print load_and_merge('/petitioner/sms/case_approval', all_data['data'], lang='he')
        print '###############################################################################'
        print load_and_merge('/petitioner/sms/second_reminder', all_data['data'], lang='he')
        print '###############################################################################'
        all_data = _load('real_world_single_volunteer.json', 'template')
        print load_and_merge('/petitioner/sms/match', all_data['data'], lang='he')
        print '###############################################################################'
        all_data = _load('real_world_volunteer_two.json', 'template')
        print load_and_merge('/petitioner/sms/first_reminder', all_data['data'], lang='he')
        print '###############################################################################'

        print "Volunteer (VIKTOR):"
        print '###############################################################################'
        all_data = _load('real_world_volunteer_two.json', 'template')
        print load_and_merge('/volunteer/sms/first_reminder', all_data['data'], lang='he')
        print '###############################################################################'
        all_data = _load('real_world_volunteer.json', 'template')
        print load_and_merge('/volunteer/sms/register_to_case', all_data['data'], lang='he')
        print '###############################################################################'
        all_data = _load('real_world_volunteer_two.json', 'template')
        print load_and_merge('/volunteer/sms/second_reminder', all_data['data'], lang='he')
        print '###############################################################################'

    # manual testing
    def single_print(self):
        print '###############################################################################'
        all_data = _load('real_world_volunteer_two.json', 'template')
        print load_and_merge('/volunteer/sms/second_reminder', all_data['data'], lang='he')
        print '###############################################################################'

    # negatives

    def test_merge_fail_1(self):
        self.assertRaises(Exception, merge, 'Hello {{name}}', None)

    def test_merge_fail_2(self):
        self.assertRaises(Exception, merge, {}, 'wrong')

    def test_merge_fail_3(self):
        self.assertRaises(Exception, merge, 'Hello {{name}} {{u_cant_find_me}}', {'name': 'jack'})

    def test_merge_fail_4(self):
        self.assertRaises(Exception, merge, 'Hello {{name}}', {'___name': 'jack'})

    def test_load_and_merge_fail_1(self):
        self.assertRaises(Exception, load_and_merge, 'test_only.jinja', {'___name': 'jack'})

    def test_load_and_merge_fail_2(self):
        self.assertRaises(Exception, load_and_merge, 'test_only.jinja', ['jack'])

    def test_load_and_merge_fail_3(self):
        self.assertRaises(Exception, load_and_merge, 'test_only.jinja', {'name': 'jack'}, lang='xyz')
