__author__ = 'avishayb'
import glob
import unittest

test_files = glob.glob('*_tests.py')
module_strings = [test_file[0:len(test_file)-3] for test_file in test_files]
suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]
testSuite = unittest.TestSuite(suites)
text_runner = unittest.TextTestRunner().run(testSuite)
print('Skipped:')
for skipped in [test for test in text_runner.skipped]:
    print(str(skipped[0]) + ' --> ' + skipped[1])
