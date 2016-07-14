from IPython.core.magic import (Magics, magics_class, line_magic)
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from .spinner import Spinner

@magics_class
class AsyncMagics(Magics):
    '''Asynchronous call of long-running IO-blocked functions using ThreadPoolExecutor
    '''

    def __init__(self, shell):
        super(AsyncMagics, self).__init__(shell)
        self.pool = ThreadPoolExecutor(2)

    @line_magic('bg')
    def lmagic(self, line):
        """Process a line with a single function call with or without assignment

        >>> %bg result = long_call()

        runs long_call() in a separate thread and creates a Spinner progress indicator.
        When finished, it updates the variable `result` in the IPython shell.

        >>> future = %bg long_call()

        Same as above but returns the future object. When `future.done()` is True,
        get the value with `future.result()`.
        """
        if '=' in line:
            lhs,rhs = (s.strip() for s in line.split('=', 1))
            progress = Spinner(lhs, timeout=300)
            progress.start()
            def done(r):
                self.shell.push({lhs: r.result()})
                progress.stop()
            future = self._execute_async(rhs, callback=done)
        else:
            rhs = line
            progress = Spinner(line, timeout=300)
            progress.start()
            future = self._execute_async(line, callback=lambda r: progress.stop())
            return future

    def _execute_async(self, rhs, callback=None):
        future = eval('self.pool.submit(%s' % rhs.replace('(', ',', 1),
                      self.shell.user_ns,
                      locals())
        future.add_done_callback(callback)
        return future
