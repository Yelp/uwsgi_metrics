"""Translated from TimerTest.java"""


import mock
import pytest

from uwsgi_metrics.histogram import Histogram
from uwsgi_metrics.meter import Meter
from uwsgi_metrics.timer import Timer


@pytest.fixture
def timer():
    histogram = mock.create_autospec(Histogram)
    meter = mock.create_autospec(Meter)

    timer = Timer('seconds')
    timer.meter = meter
    timer.histogram = histogram
    return timer


def test_get_count(timer):
    timer.histogram.get_count.return_value = mock.sentinel.count
    assert timer.get_count() == mock.sentinel.count


def test_get_mean_rate(timer):
    timer.meter.get_mean_rate.return_value = mock.sentinel.mean_rate
    assert timer.get_mean_rate() == mock.sentinel.mean_rate


def test_get_one_minute_rate(timer):
    timer.meter.get_one_minute_rate.return_value = \
        mock.sentinel.one_minute_rate
    assert timer.get_one_minute_rate(), mock.sentinel.one_minute_rate


def test_get_five_minute_rate(timer):
    timer.meter.get_five_minute_rate.return_value = \
        mock.sentinel.five_minute_rate
    assert timer.get_five_minute_rate() == mock.sentinel.five_minute_rate


def test_get_fifteen_minute_rate(timer):
    timer.meter.get_fifteen_minute_rate.return_value = \
        mock.sentinel.fifteen_minute_rate
    assert timer.get_fifteen_minute_rate() == mock.sentinel.fifteen_minute_rate


def test_update_modifies_histogram_and_meter(timer):
    timer.update(mock.sentinel.timer_update_value)
    timer.histogram.update.assert_called_once_with(
        mock.sentinel.timer_update_value)
    timer.meter.mark.assert_called_once_with()


def test_snapshot_is_returned(timer):
    timer.histogram.get_snapshot.return_value = mock.sentinel.snapshot
    assert timer.get_snapshot() == mock.sentinel.snapshot


def test_update_ignores_negative_values(timer):
    timer.update(-1)
    assert not timer.histogram.update.called
    assert not timer.meter.mark.called


def test_view(timer):
    timer.meter.get_count.return_value = mock.sentinel.count
    timer.meter.get_fifteen_minute_rate.return_value = mock.sentinel.m15_rate
    timer.meter.get_one_minute_rate.return_value = mock.sentinel.m1_rate
    timer.meter.get_five_minute_rate.return_value = mock.sentinel.m5_rate
    timer.meter.get_mean_rate.return_value = mock.sentinel.mean_rate

    mock_snapshot = mock.Mock()
    mock_snapshot.get_max.return_value = mock.sentinel.max
    mock_snapshot.get_mean.return_value = mock.sentinel.mean
    mock_snapshot.get_min.return_value = mock.sentinel.min
    mock_snapshot.get_median.return_value = mock.sentinel.median
    mock_snapshot.get_75th_percentile.return_value = mock.sentinel.p75
    mock_snapshot.get_95th_percentile.return_value = mock.sentinel.p95
    mock_snapshot.get_98th_percentile.return_value = mock.sentinel.p98
    mock_snapshot.get_99th_percentile.return_value = mock.sentinel.p99
    mock_snapshot.get_999th_percentile.return_value = mock.sentinel.p999
    mock_snapshot.get_std_dev.return_value = mock.sentinel.stddev
    timer.histogram.get_snapshot.return_value = mock_snapshot

    expected = {
        'count': mock.sentinel.count,
        'max': mock.sentinel.max,
        'mean': mock.sentinel.mean,
        'min': mock.sentinel.min,
        'p50': mock.sentinel.median,
        'p75': mock.sentinel.p75,
        'p95': mock.sentinel.p95,
        'p98': mock.sentinel.p98,
        'p99': mock.sentinel.p99,
        'p999': mock.sentinel.p999,
        'stddev': mock.sentinel.stddev,
        'm15_rate': mock.sentinel.m15_rate,
        'm1_rate': mock.sentinel.m1_rate,
        'm5_rate': mock.sentinel.m5_rate,
        'mean_rate': mock.sentinel.mean_rate,
        'duration_units': 'seconds',
        'rate_units': 'calls/second'
    }

    assert timer.view() == expected
