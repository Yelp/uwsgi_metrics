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
    timer.histogram.view.return_value = mock.sentinel.histogram_view
    timer.meter.view.return_value = mock.sentinel.meter_view
    expected = {
        'duration': mock.sentinel.histogram_view,
        'rate': mock.sentinel.meter_view,
        'type': 'timer',
    }
    assert timer.view() == expected
