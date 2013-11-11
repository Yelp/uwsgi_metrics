# This is the uWSGI-specific part of uwsgi_metrics.

import contextlib
import logging
import marshal
import mmap
import time

try:
    import uwsgi
except ImportError:
    # The uwsgi module is only available when running under uWSGI.
    # Mock it out for tests and documentation building.
    class uwsgi(object):
        @staticmethod
        def lock():
            pass

        @staticmethod
        def unlock():
            pass

        @staticmethod
        def masterpid():
            return 42

try:
    import uwsgidecorators
except ImportError:
    class uwsgidecorators(object):
        @staticmethod
        def mulefunc(target):
            def decorator(fun):
                return fun
            return decorator

        @staticmethod
        def timer(period, target):
            def decorator(fun):
                return fun
            return decorator

from uwsgi_metrics.histogram import Histogram
from uwsgi_metrics.timer import Timer


# Interval between updating marshalled metrics
PROCESSING_PERIOD_S = 1

# Maximum size of marshalled metrics
MAX_MARSHALLED_VIEW_SIZE = 2**20

log = logging.getLogger('uwsgi_metrics.metrics')

# Dictionaries of metrics objects living in mule, periodically marshalled to
# memory mapped buffer for viewing by regular workers.
timers = {}
histograms = {}

# The memory mapped buffer
marshalled_metrics_mmap = mmap.mmap(-1, MAX_MARSHALLED_VIEW_SIZE)
marshalled_metrics_mmap.write(
    marshal.dumps({
        'timers': {},
        'histograms': {}
        }))


@uwsgidecorators.timer(PROCESSING_PERIOD_S, target='mule1')
def periodically_write_metrics_to_mmaped_buffer(_):
    view = {
        'timers': {},
        'histograms': {}
        }
    for name, timer in timers.iteritems():
        view['timers'][name] = timer.view()
    for name, histogram in histograms.iteritems():
        view['histograms'][name] = histogram.view()

    marshalled_view = marshal.dumps(view)
    if len(marshalled_view) > MAX_MARSHALLED_VIEW_SIZE:
        log.warn(
            'Marshalled length too large, got %d, max %d. '
            'Try recording fewer metrics or increasing '
            'MAX_MARSHALLED_VIEW_SIZE'
            % (len(marshalled_view), MAX_MARSHALLED_VIEW_SIZE))
        return
    marshalled_metrics_mmap.seek(0)
    try:
        # Reading and writing to/from an mmap'ed buffer is not guaranteed
        # to be atomic, so we must serialize access to it.
        uwsgi.lock()
        marshalled_metrics_mmap.write(marshalled_view)
    finally:
        uwsgi.unlock()


def view():
    """Get a dictionary representation of current metrics."""
    marshalled_metrics_mmap.seek(0)
    try:
        uwsgi.lock()
        marshalled_view = marshalled_metrics_mmap.read(
            MAX_MARSHALLED_VIEW_SIZE)
    finally:
        uwsgi.unlock()
    return marshal.loads(marshalled_view)


@contextlib.contextmanager
def timer(name):
    """
    Context manager to time a section of code::

        from uwsgi_metrics import timer
        with timer('my_timer'):
            do_some_operation()
    """
    start_time = time.time()
    yield
    end_time = time.time()
    delta = end_time - start_time
    handle_timer(name, delta)


@uwsgidecorators.mulefunc(1)
def handle_timer(name, delta):
    # This asynchronously runs in the mule
    if not name in timers:
        timers[name] = Timer()
    timers[name].update(delta)


@uwsgidecorators.mulefunc(1)
def histogram(name, value):
    """
    Record a value in a histogram:
    ::

        from uwsgi_metrics import histogram
        histogram('my_histogram', len(queue))
    """
    if not name in histograms:
        histograms[name] = Histogram()
    histograms[name].update(value)
