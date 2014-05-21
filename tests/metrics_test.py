import mock
import pytest

import uwsgi_metrics
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
        'tests.metrics_test': {
            'my_timer': {
                'duration': {
                    'p98': 0.0,
                    'p99': 0.0,
                    'p75': 0.0,
                    'min': 0.0,
                    'max': 0.0,
                    'median': 0.0,
                    'p95': 0.0,
                    'std_dev': 0.0,
                    'p999': 0.0,
                    'unit': 'milliseconds',
                    'mean': 0.0,
                },
                'rate': {
                    'count': 1,
                    'm5': 0.0,
                    'm15': 0.0,
                    'm1': 0.0,
                    'unit': 'seconds',
                    'mean': 0.0,
                },
                'type': 'timer',
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
        'tests.metrics_test': {
            'my_timer': {
                'duration': {
                    'p98': 0.0,
                    'p99': 0.0,
                    'p75': 0.0,
                    'min': 0.0,
                    'max': 0.0,
                    'median': 0.0,
                    'p95': 0.0,
                    'std_dev': 0.0,
                    'p999': 0.0,
                    'unit': 'milliseconds',
                    'mean': 0.0,
                },
                'rate': {
                    'count': 1,
                    'm5': 0.0,
                    'm15': 0.0,
                    'm1': 0.0,
                    'unit': 'seconds',
                    'mean': 0.0,
                    },
                'type': 'timer',
            }
        }
    }

    assert expected == actual


def test_histogram(setup):
    uwsgi_metrics.histogram(__name__, 'my_histogram', 42.0)
    emit(None)

    actual = uwsgi_metrics.view()
    expected = {
        'tests.metrics_test': {
            'my_histogram': {
                'max': 42.0,
                'mean': 42.0,
                'median': 42.0,
                'min': 42.0,
                'p75': 42.0,
                'p95': 42.0,
                'p98': 42.0,
                'p99': 42.0,
                'p999': 42.0,
                'std_dev': 0.0,
                'count': 1,
                'type': 'histogram',
            }
        }
    }

    assert expected == actual


def test_counter(setup):
    uwsgi_metrics.counter(__name__, 'my_counter', 17.0)
    emit(None)

    actual = uwsgi_metrics.view()
    expected = {
        'tests.metrics_test': {
            'my_counter': {
                'count': 17.0,
                'type': 'counter',
            }
        }
    }

    assert expected == actual


def test_meter(setup):
    with mock.patch('time.time', return_value=42.0):
        uwsgi_metrics.meter(__name__, 'my_meter', 'my_event_type')
        emit(None)

    actual = uwsgi_metrics.view()
    expected = {
        'tests.metrics_test': {
            'my_meter': {
                'count': 1,
                'm5': 0.0,
                'm15': 0.0,
                'm1': 0.0,
                'mean': 0.0,
                'event_type': 'my_event_type',
                'type': 'meter',
                'unit': 'seconds',
            }
        }
    }

    assert expected == actual
