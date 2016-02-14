import unittest

from org.gi.server.services.templates import merge


class GITemplateTestCase(unittest.TestCase):

    def test_merge(self):
        self.assertEqual(merge('Hello {{name}}', {'name': 'jack'}), 'Hello jack')

    def test_merge_fail_1(self):
        self.assertRaises(Exception, merge, 'Hello {{name}}', None)

    def test_merge_fail_2(self):
        self.assertRaises(Exception, merge, {}, 'wrong')

    def test_merge_fail_3(self):
        self.assertRaises(Exception, merge, 'Hello {{name}} {{u_cant_find_me}}', {'name': 'jack'})

    def test_merge_fail_4(self):
        self.assertRaises(Exception, merge, 'Hello {{name}}', {'___name': 'jack'})


