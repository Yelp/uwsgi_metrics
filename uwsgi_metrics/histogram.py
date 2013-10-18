from uwsgi_metrics.counter import Counter
from uwsgi_metrics.reservoir import Reservoir


class Histogram(object):
    """A metric which calculates the distribution of a value.

    Translated from Histogram.java
    """

    def __init__(self, counter=None, reservoir=None):
        self.counter = counter or Counter()
        self.reservoir = reservoir or Reservoir()

    def update(self, value):
        self.counter.inc()
        self.reservoir.update(value)

    def get_count(self):
        return self.counter.get_count()

    def get_snapshot(self):
        return self.reservoir.get_snapshot()
