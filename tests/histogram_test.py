# -*- coding: utf-8 -*-
"""Translated from HistogramTest.java"""
from __future__ import absolute_import
from __future__ import unicode_literals

try:
    from unittest import mock
except:
    import mock
import pytest

from uwsgi_metrics.histogram import Histogram
from uwsgi_metrics.reservoir import Reservoir
from uwsgi_metrics.snapshot import Snapshot


@pytest.fixture
def histogram():
    reservoir = mock.create_autospec(Reservoir)
    histogram = Histogram()
    histogram.reservoir = reservoir
    return histogram


def test_updates_the_count_on_updates(histogram):
    assert histogram.get_count() == 0
    histogram.update(1)
    assert histogram.get_count() == 1


def test_returns_the_snapshot_from_the_reservoir(histogram):
    histogram.get_snapshot()
    histogram.reservoir.get_snapshot.assert_called_once_with()


def test_updates_the_reservoir(histogram):
    histogram.update(1)
    histogram.reservoir.update.assert_called_once_with(1)


def test_view(histogram):
    snapshot = mock.create_autospec(Snapshot)
    snapshot.view.return_value = {'foo': 42}
    histogram.reservoir.get_snapshot.return_value = snapshot
    expected = {
        'foo': 42,
        'count': 0,
    }
    assert histogram.view() == expected
