from IPython.display import display
from ipywidgets import Text
import threading
import itertools
import time

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self.__stop = threading.Event()

    def stop(self, val=None):
        self.__stop.set()

    def stopped(self):
        return self.__stop.isSet()

class Spinner(object):
    '''Threaded progress indicator
    '''
    spinner_str = itertools.cycle('|/-\\')

    def __init__(self, name, timeout=3, update_time=.1):
        self.name = name
        self.timeout = timeout
        self.max_loops = int(timeout / update_time) + 1
        self.update_time = update_time
        self.thread = StoppableThread(target=self._run, name=name)

    def _run(self):
        text = Text(border_style='None', font_family='courier')
        display(text)
        t = 0
        while self.timeout is None or t <= self.timeout:
            t += self.update_time
            if self.thread.stopped():
                text.value = 'Task "%s" DONE ' % self.name
                break
            elapsed_time = '  ({:.1f} seconds)'.format(time.time() - self.start_time)
            text.value = 'Task "%s" running...' % self.name + next(self.spinner_str) + elapsed_time
            time.sleep(self.update_time)
        else:
            text.value = 'TIMEOUT'

    def start(self):
        self.start_time = time.time()
        self.thread.start()
        return self.thread

    def stop(self):
        self.thread.stop()
