import threading


def get_scheduler(sleep_time_sec,action, *args):
    """
    Get an instance of a Scheduler
    :param sleep_time_sec: Number of seconds to wait between each execution
    :param action: A function to be executed every sleep_time_sec
    :param args: The function arguments
    :return:a Scheduler and a stopper event

    Example:

    def foo(_input):
        _input[0]['cnt'] = _input[0]['cnt'] + 1
        print('Inside foo: ' + str(_input[0]))

    data = {'cnt': 0}
    scheduler, stopper = get_scheduler(3, foo, data)
    scheduler.start()
    cnt = 0
    import time
    while cnt < 10:
        time.sleep(1)
        cnt += 1
    print('The end: ' + str(data))
    stopper.set()


    """
    stop = threading.Event()
    scheduler = Scheduler(stop, sleep_time_sec,action, *args)
    scheduler.setDaemon(True)
    return scheduler, stop


class Scheduler(threading.Thread):
    def __init__(self, event, sleep_time_sec,action, *args):
        threading.Thread.__init__(self)
        if not event or not isinstance(event, threading._Event):
            raise Exception('event must be a threading.Event')
        if not sleep_time_sec or not isinstance(sleep_time_sec, int) or not sleep_time_sec > 0:
            raise Exception('sleep_time_sec must be positive integer')
        if not action or not hasattr(action, '__call__'):
            raise Exception('action must be a function')
        self.stopped = event
        self.sleep_time_sec = sleep_time_sec
        self.action = action
        self.args = args

    def run(self):
        while not self.stopped.wait(self.sleep_time_sec):
            self.action(self.args)


