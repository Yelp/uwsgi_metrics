import mock
import testify as T

from uwsgi_metrics.meter import Meter

MAX_DIFFERENCE = 0.001


class Clock(object):
    def __init__(self, time):
        self._time = time

    def __call__(self):
        return self._time

    def add_seconds(self, seconds):
        self._time += seconds


class MeterTest(T.TestCase):
    """Translated from MeterTest.java"""

    @T.setup_teardown
    def setup_mocks(self):
        with mock.patch('time.time', Clock(0.0)) as clock:
            self.clock = clock
            self.meter = Meter()
            yield

    def assert_almost_equal(self, lval, rval, max_difference):
        T.assert_lte(abs(lval - rval), max_difference)

    def test_starts_out_with_no_rates_or_count(self):
        self.clock.add_seconds(10)
        T.assert_equal(self.meter.get_count(), 0)
        T.assert_equal(self.meter.get_mean_rate(), 0.0)
        T.assert_equal(self.meter.get_one_minute_rate(), 0.0)
        T.assert_equal(self.meter.get_five_minute_rate(), 0.0)
        T.assert_equal(self.meter.get_fifteen_minute_rate(), 0.0)

    def test_marks_events_and_updates_rates_and_count(self):
        self.meter.mark()
        self.clock.add_seconds(10)
        self.meter.mark(2)
        T.assert_equal(self.meter.get_mean_rate(), 0.3)
        self.assert_almost_equal(self.meter.get_one_minute_rate(), 0.1840,
                                 MAX_DIFFERENCE)
        self.assert_almost_equal(self.meter.get_five_minute_rate(), 0.1966,
                                 MAX_DIFFERENCE)
        self.assert_almost_equal(self.meter.get_fifteen_minute_rate(), 0.1988,
                                 MAX_DIFFERENCE)

    def test_view(self):
        T.assert_equal(self.meter.view(),
                       {'m1': 0.0,
                        'm5': 0.0,
                        'm15': 0.0,
                        'mean': 0.0,
                        'count': 0
                        })
