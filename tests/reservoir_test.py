import mock
import testify as T

from uwsgi_metrics.reservoir import Reservoir


class ReservoirTest(T.TestCase):
    """Translated from ExponentiallyDecayingReservoirTest.java"""

    def assert_all_values_between(self, reservoir, low, high):
        for value in reservoir.get_snapshot().values:
            T.assert_gte(value, low)
            T.assert_lt(value, high)

    def test_insert_1000_elements_into_a_reservoir_of_100(self):
        reservoir = Reservoir(size=100, alpha=0.99)
        for i in xrange(1000):
            reservoir.update(i)

        T.assert_equal(reservoir.get_snapshot().size(), 100)
        self.assert_all_values_between(reservoir, 0, 1000)

    def test_insert_10_elements_into_a_reservoir_of_100(self):
        reservoir = Reservoir(size=100, alpha=0.99)
        for i in xrange(10):
            reservoir.update(i)

        T.assert_equal(reservoir.get_snapshot().size(), 10)
        self.assert_all_values_between(reservoir, 0, 10)

    def test_insert_100_elemnts_into_a_heavily_baised_reservoir_of_1000(self):
        reservoir = Reservoir(size=1000, alpha=0.01)
        for i in xrange(100):
            reservoir.update(i)

        T.assert_equal(reservoir.get_snapshot().size(), 100)
        self.assert_all_values_between(reservoir, 0, 100)

    def test_inactivity_should_not_corrupt_sampling_state(self):

        class Clock(object):
            def __init__(self, time):
                self._time = time

            def __call__(self):
                return self._time

            def add_millis(self, millis):
                self._time += 0.001 * millis

            def add_hours(self, hours):
                self._time += 60 * 60 * hours

        with mock.patch('uwsgi_metrics.reservoir.Reservoir'
                        + '.current_time_in_fractional_seconds',
                        Clock(42.0)) as clock:
            reservoir = Reservoir(size=10, alpha=0.015)

            # Add 1000 values at a rate of 10 values/second
            for i in xrange(1000):
                reservoir.update(1000 + i)
                clock.add_millis(100)

            T.assert_equal(reservoir.get_snapshot().size(), 10)
            self.assert_all_values_between(reservoir, 1000, 2000)

            # Wait for 15 hours and add another value.  This should trigger a
            # rescale. Note that the number of samples will be reduced to 2
            # because of the very small scaling factor that will make all
            # existing priorities equal to zero after rescale.
            clock.add_hours(15)
            reservoir.update(2000)
            T.assert_equal(reservoir.get_snapshot().size(), 2)
            self.assert_all_values_between(reservoir, 1000, 3000)
