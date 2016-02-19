import unittest

from org.gi.server.service.scheduler import get_scheduler
import time


class GISchedulerTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GISchedulerTestCase, self).__init__(*args, **kwargs)
        self.test_mode = True

    def test_scheduler(self):
        def foo(_data):
            _data[0]['cnt'] += 1

        data = {'cnt': 0}
        scheduler, stop = get_scheduler(1, foo, data)
        seconds = 0
        scheduler.start()
        # The loop below simulates server main loop
        # While the loop is active the scheduler thread is calling 'foo' every 1 sec
        # As a result the value of 'cnt' field in 'data' is incremented
        while seconds < 3:
            time.sleep(1)
            seconds += 1
        # Ask the scheduler to stop running
        stop.set()
        # Make sure 'cnt' was incremented
        self.assertTrue(1 < data['cnt'] <= 3, 'The value of cnt field is %d' % data['cnt'])
