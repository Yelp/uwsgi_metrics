import mock
import testify as T

from uwsgi_metrics.histogram import Histogram
from uwsgi_metrics.reservoir import Reservoir
from uwsgi_metrics.snapshot import Snapshot


class HistogramTest(T.TestCase):
    """Translated from HistogramTest.java"""

    @T.setup
    def setup(self):
        self.reservoir = mock.create_autospec(Reservoir)
        self.histogram = Histogram(reservoir=self.reservoir)

    def test_updates_the_count_on_updates(self):
        T.assert_equal(self.histogram.get_count(), 0)
        self.histogram.update(1)
        T.assert_equal(self.histogram.get_count(), 1)

    def test_returns_the_snapshot_from_the_reservoir(self):
        self.histogram.get_snapshot()
        self.reservoir.get_snapshot.assert_called_once_with()

    def test_updates_the_reservoir(self):
        self.histogram.update(1)
        self.reservoir.update.assert_called_once_with(1)

    def test_view(self):
        snapshot = mock.create_autospec(Snapshot)
        snapshot.view.return_value = {'foo': 42}
        self.reservoir.get_snapshot.return_value = snapshot
        T.assert_equal(self.histogram.view(),
                       {'foo': 42,
                        'count': 0
                        })
