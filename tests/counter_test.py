import testify as T

from uwsgi_metrics.counter import Counter


class CounterTest(T.TestCase):
    """Translated from CounterTest.java"""

    @T.setup
    def create_counter(self):
        self.counter = Counter()

    def test_starts_at_zero(self):
        T.assert_equal(self.counter.get_count(), 0)

    def test_increments_by_one(self):
        self.counter.inc()
        T.assert_equal(self.counter.get_count(), 1)

    def test_increments_by_an_arbitrary_delta(self):
        self.counter.inc(12)
        T.assert_equal(self.counter.get_count(), 12)

    def test_decrements_by_one(self):
        self.counter.dec()
        T.assert_equal(self.counter.get_count(), -1)

    def test_decrements_by_an_arbitrary_delta(self):
        self.counter.dec(12)
        T.assert_equal(self.counter.get_count(), -12)

    def test_view(self):
        self.counter.inc(13)
        T.assert_equal(self.counter.view(),
                       {'count': 13})
