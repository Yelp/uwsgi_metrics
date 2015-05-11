# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    from unittest import mock
except:
    import mock
import pytest

import uwsgi_metrics
from uwsgi_metrics.__about__ import __version__
from uwsgi_metrics.metrics import emit


@pytest.fixture
def setup():
    uwsgi_metrics.metrics.reset()
    uwsgi_metrics.initialize()


def test_timing(setup):
    with mock.patch('time.time', return_value=42.0):
        with uwsgi_metrics.timing(__name__, 'my_timer'):
            pass
        emit(None)

    actual = uwsgi_metrics.view()
    expected = {
        'version': __version__,
        'counters': {},
        'gauges': {},
        'histograms': {},
        'meters': {},
        'timers': {
            'tests.metrics_test.my_timer': {
                'count': 1,
                'max': 0.0,
                'mean': 0.0,
                'min': 0.0,
                'p50': 0.0,
                'p75': 0.0,
                'p95': 0.0,
                'p98': 0.0,
                'p99': 0.0,
                'p999': 0.0,
                'stddev': 0.0,
                'm15_rate': 0.0,
                'm1_rate': 0.0,
                'm5_rate': 0.0,
                'mean_rate': 0.0,
                'duration_units': 'milliseconds',
                'rate_units': 'calls/second',
            }
        }
    }

    assert expected == actual


def test_timer(setup):
    with mock.patch('time.time', return_value=42.0):
        uwsgi_metrics.timer(__name__, 'my_timer', 0.0)
        emit(None)

    actual = uwsgi_metrics.view()

    expected = {
        'version': __version__,
        'counters': {},
        'gauges': {},
        'histograms': {},
        'meters': {},
        'timers': {
            'tests.metrics_test.my_timer': {
                'count': 1,
                'max': 0.0,
                'mean': 0.0,
                'min': 0.0,
                'p50': 0.0,
                'p75': 0.0,
                'p95': 0.0,
                'p98': 0.0,
                'p99': 0.0,
                'p999': 0.0,
                'stddev': 0.0,
                'm15_rate': 0.0,
                'm1_rate': 0.0,
                'm5_rate': 0.0,
                'mean_rate': 0.0,
                'duration_units': 'milliseconds',
                'rate_units': 'calls/second',
            }
        }
    }

    assert expected == actual


def test_histogram(setup):
    uwsgi_metrics.histogram(__name__, 'my_histogram', 42.0)
    emit(None)

    actual = uwsgi_metrics.view()
    expected = {
        'version': __version__,
        'counters': {},
        'gauges': {},
        'meters': {},
        'timers': {},
        'histograms': {
            'tests.metrics_test.my_histogram': {
                'count': 1,
                'max': 42.0,
                'mean': 42.0,
                'min': 42.0,
                'p50': 42.0,
                'p75': 42.0,
                'p95': 42.0,
                'p98': 42.0,
                'p99': 42.0,
                'p999': 42.0,
                'stddev': 0.0,
            }
        }
    }

    assert expected == actual


def test_counter(setup):
    uwsgi_metrics.counter(__name__, 'my_counter', 17.0)
    emit(None)

    actual = uwsgi_metrics.view()
    expected = {
        'version': __version__,
        'gauges': {},
        'histograms': {},
        'meters': {},
        'timers': {},
        'counters': {
            'tests.metrics_test.my_counter': {
                'count': 17.0,
            }
        }
    }

    assert expected == actual


def test_meter(setup):
    with mock.patch('time.time', return_value=42.0):
        uwsgi_metrics.meter(__name__, 'my_meter')
        emit(None)

    actual = uwsgi_metrics.view()
    expected = {
        'version': __version__,
        'counters': {},
        'gauges': {},
        'histograms': {},
        'timers': {},
        'meters': {
            'tests.metrics_test.my_meter': {
                'count': 1,
                'm15_rate': 0.0,
                'm1_rate': 0.0,
                'm5_rate': 0.0,
                'mean_rate': 0.0,
                'units': 'events/second',
            }
        }
    }

    assert expected == actual
