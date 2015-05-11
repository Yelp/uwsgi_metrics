# -*- coding: utf-8 -*-
"""Translated from CounterTest.java"""
from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from uwsgi_metrics.counter import Counter


@pytest.fixture
def counter():
    return Counter()


def test_starts_at_zero(counter):
    assert counter.get_count() == 0


def test_increments_by_one(counter):
    counter.inc()
    assert counter.get_count() == 1


def test_increments_by_an_arbitrary_delta(counter):
    counter.inc(12)
    assert counter.get_count() == 12


def test_decrements_by_one(counter):
    counter.dec()
    assert counter.get_count() == -1


def test_decrements_by_an_arbitrary_delta(counter):
    counter.dec(12)
    assert counter.get_count() == -12


def test_view(counter):
    counter.inc(13)
    assert counter.view() == {'count': 13}
