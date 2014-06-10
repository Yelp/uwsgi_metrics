"""Translated from SnapshotTest.java"""


import random

import pytest

from uwsgi_metrics.snapshot import Snapshot


@pytest.fixture
def snapshot():
    return Snapshot([5, 1, 2, 3, 4])


def test_small_quantiles_are_the_first_value(snapshot):
    assert snapshot.get_value(0.0) == 1


def test_big_quantiles_are_the_last_value(snapshot):
    assert snapshot.get_value(1.0) == 5


def test_has_a_median(snapshot):
    assert snapshot.get_median() == 3


def test_has_a_75th_percentile(snapshot):
    assert snapshot.get_75th_percentile() == 4.5


def test_has_a_95th_percentile(snapshot):
    assert snapshot.get_95th_percentile() == 5.0


def test_has_a_98th_percentile(snapshot):
    assert snapshot.get_98th_percentile() == 5.0


def test_has_a_99th_percentile(snapshot):
    assert snapshot.get_99th_percentile() == 5.0


def test_has_a_999th_percentile(snapshot):
    assert snapshot.get_999th_percentile() == 5.0


def test_has_values(snapshot):
    assert snapshot.values == [1, 2, 3, 4, 5]


def test_has_a_size(snapshot):
    assert snapshot.size() == 5


def test_calculates_the_minimum_value(snapshot):
    assert snapshot.get_min() == 1


def test_calculates_the_maximum_value(snapshot):
    assert snapshot.get_max() == 5


def test_calculates_the_std_dev(snapshot):
    assert abs(snapshot.get_std_dev() - 1.5811) < 0.0001


def test_calculates_a_min_of_zero_for_an_empty_snapshot():
    assert Snapshot().get_min() == 0


def test_calculates_a_max_of_zero_for_an_empty_snapshot():
    assert Snapshot().get_max() == 0


def test_calculates_a_mean_of_zero_for_an_empty_snapshot():
    assert Snapshot().get_mean() == 0


def test_calculates_a_std_dev_of_zero_for_an_empty_snapshot():
    assert Snapshot().get_std_dev() == 0


def test_calculates_a_std_dev_of_zero_for_a_singelton_snapshot():
    assert Snapshot([1]).get_std_dev() == 0


def test_all_percentiles_in_more_detail():
    values = range(0, 1000)
    random.shuffle(values)
    snapshot = Snapshot(values)

    tolerance = 1
    assert snapshot.values == sorted(values)
    assert snapshot.size() == 1000
    assert snapshot.get_value(0.0) == 0
    assert snapshot.get_value(1.0) == 999
    assert snapshot.get_median() == 499.5
    assert abs(snapshot.get_75th_percentile() - 750) < tolerance
    assert abs(snapshot.get_98th_percentile() - 980) < tolerance
    assert abs(snapshot.get_99th_percentile() - 990) < tolerance
    assert abs(snapshot.get_999th_percentile() - 999) < tolerance


def test_view(snapshot):
    view = snapshot.view()
    assert view['max'] == 5
    assert view['mean'] == 3.0
    assert view['min'] == 1
    assert view['p50'] == 3.0
    assert view['p75'] == 4.5
    assert view['p98'] == 5
    assert view['p99'] == 5
    assert view['p999'] == 5
    assert abs(view['stddev'] - 1.5811) < 0.0001
