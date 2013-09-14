import random

import testify as T

from uwsgi_metrics.snapshot import Snapshot

# A small value
EPSILON = 0.01

class SnapshotTest(T.TestCase):
    """Translated from https://github.com/codahale/metrics/blob/master/metrics-core/src/test/java/com/codahale/metrics/SnapshotTest.java"""

    @T.setup
    def create_snapshot(self):
        self.snapshot = Snapshot([5, 1, 2, 3, 4])

    def test_small_quantiles_are_the_first_value(self):
        T.assert_equal(self.snapshot.get_value(0.0), 1)

    def test_big_quantiles_are_the_last_value(self):
        T.assert_equal(self.snapshot.get_value(1.0), 5)

    def test_has_a_median(self):
        T.assert_equal(self.snapshot.get_median(), 3)

    def test_has_a_75th_percentile(self):
        T.assert_equal(self.snapshot.get_75th_percentile(), 4.5)

    def test_has_a_95th_percentile(self):
        T.assert_equal(self.snapshot.get_95th_percentile(), 5.0)

    def test_has_a_98th_percentile(self):
        T.assert_equal(self.snapshot.get_98th_percentile(), 5.0)

    def test_has_a_99th_percentile(self):
        T.assert_equal(self.snapshot.get_99th_percentile(), 5.0)

    def test_has_a_999th_percentile(self):
        T.assert_equal(self.snapshot.get_999th_percentile(), 5.0)

    def test_has_values(self):
        T.assert_equal(self.snapshot.values, [1, 2, 3, 4, 5])

    def test_has_a_size(self):
        T.assert_equal(self.snapshot.size(), 5)

    def test_calculates_the_minimum_value(self):
        T.assert_equal(self.snapshot.get_min(), 1)

    def test_calculates_the_maximum_value(self):
        T.assert_equal(self.snapshot.get_max(), 5)

    def test_calculates_the_std_dev(self):
        T.assert_almost_equal(self.snapshot.get_std_dev(), 1.5811, 4)

    def test_calculates_a_min_of_zero_for_an_empty_snapshot(self):
        T.assert_equal(Snapshot().get_min(), 0)

    def test_calculates_a_max_of_zero_for_an_empty_snapshot(self):
        T.assert_equal(Snapshot().get_max(), 0)

    def test_calculates_a_mean_of_zero_for_an_empty_snapshot(self):
        T.assert_equal(Snapshot().get_mean(), 0)

    def test_calculates_a_std_dev_of_zero_for_an_empty_snapshot(self):
        T.assert_equal(Snapshot().get_std_dev(), 0)

    def test_calculates_a_std_dev_of_zero_for_a_singelton_snapshot(self):
        T.assert_equal(Snapshot([1]).get_std_dev(), 0)

    def test_all_percentiles_in_more_detail(self):
        values = range(0, 1000)
        random.shuffle(values)
        self.snapshot = Snapshot(values)

        T.assert_equal(self.snapshot.values, sorted(values))
        T.assert_equal(self.snapshot.size(), 1000)
        T.assert_equal(self.snapshot.get_value(0.0), 0)
        T.assert_equal(self.snapshot.get_value(1.0), 999)
        T.assert_equal(self.snapshot.get_median(), 499.5)
        T.assert_within_tolerance(self.snapshot.get_75th_percentile(), 750, EPSILON)
        T.assert_within_tolerance(self.snapshot.get_98th_percentile(), 980, EPSILON)
        T.assert_within_tolerance(self.snapshot.get_99th_percentile(), 990, EPSILON)
        T.assert_within_tolerance(self.snapshot.get_999th_percentile(), 999, EPSILON)
