import mock
import testify as T

from uwsgi_metrics.timer import Timer


class TimerTest(T.TestCase):
    """Translated from TimerTest.java"""

    @T.setup
    def setup_timer(self):
        self.histogram = mock.Mock()
        self.meter = mock.Mock()
        self.timer = Timer(meter=self.meter, histogram=self.histogram)

    def test_get_count(self):
        self.histogram.get_count.return_value = mock.sentinel.count
        T.assert_equal(self.timer.get_count(), mock.sentinel.count)

    def test_get_mean_rate(self):
        self.meter.get_mean_rate.return_value = mock.sentinel.mean_rate
        T.assert_equal(self.timer.get_mean_rate(), mock.sentinel.mean_rate)

    def test_get_one_minute_rate(self):
        self.meter.get_one_minute_rate.return_value = \
            mock.sentinel.one_minute_rate
        T.assert_equal(self.timer.get_one_minute_rate(),
                       mock.sentinel.one_minute_rate)

    def test_get_five_minute_rate(self):
        self.meter.get_five_minute_rate.return_value = \
            mock.sentinel.five_minute_rate
        T.assert_equal(self.timer.get_five_minute_rate(),
                       mock.sentinel.five_minute_rate)

    def test_get_fifteen_minute_rate(self):
        self.meter.get_fifteen_minute_rate.return_value = \
            mock.sentinel.fifteen_minute_rate
        T.assert_equal(self.timer.get_fifteen_minute_rate(),
                       mock.sentinel.fifteen_minute_rate)

    def test_update_modifies_histogram_and_meter(self):
        self.timer.update()
        self.histogram.update.assert_called_once_with(1)
        self.meter.mark.assert_called_once_with()

    def test_snapshot_is_returned(self):
        self.histogram.get_snapshot.return_value = mock.sentinel.snapshot
        T.assert_equal(self.timer.get_snapshot(), mock.sentinel.snapshot)

    def test_update_ignores_negative_values(self):
        self.timer.update(-1)
        T.assert_equal(self.histogram.update.called, False)
        T.assert_equal(self.histogram.mark.called, False)
