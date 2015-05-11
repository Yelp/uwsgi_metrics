# -*- coding: utf-8 -*-
"""Translated from MeterTest.java"""
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    from unittest import mock
except:
    import mock
import pytest

from uwsgi_metrics.meter import Meter


class Clock(object):
    def __init__(self, time):
        self._time = time

    def __call__(self):
        return self._time

    def add_seconds(self, seconds):
        self._time += seconds


@pytest.yield_fixture
def meter_and_clock():
    with mock.patch('time.time', Clock(0.0)) as clock:
        clock = clock
        meter = Meter()
        yield (meter, clock)


def test_starts_out_with_no_rates_or_count(meter_and_clock):
    meter, clock = meter_and_clock[0], meter_and_clock[1]

    clock.add_seconds(10)
    assert meter.get_count() == 0
    assert meter.get_mean_rate() == 0.0
    assert meter.get_one_minute_rate() == 0.0
    assert meter.get_five_minute_rate() == 0.0
    assert meter.get_fifteen_minute_rate() == 0.0


def test_marks_events_and_updates_rates_and_count(meter_and_clock):
    def assert_almost_equal(lval, rval):
        assert abs(lval - rval) <= 0.001

    meter, clock = meter_and_clock[0], meter_and_clock[1]

    meter.mark()
    clock.add_seconds(10)
    meter.mark(2)
    assert meter.get_mean_rate() == 0.3
    assert_almost_equal(meter.get_one_minute_rate(), 0.1840)
    assert_almost_equal(meter.get_five_minute_rate(), 0.1966)
    assert_almost_equal(meter.get_fifteen_minute_rate(), 0.1988)


def test_view(meter_and_clock):
    meter = meter_and_clock[0]
    expected = {
        'count': 0,
        'm15_rate': 0.0,
        'm1_rate': 0.0,
        'm5_rate': 0.0,
        'mean_rate': 0.0,
        'units': 'events/second',
    }
    assert meter.view() == expected
