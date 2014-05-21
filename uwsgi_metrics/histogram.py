from uwsgi_metrics.reservoir import Reservoir


class Histogram(object):
    """A metric which calculates the distribution of a value.

    Translated from Histogram.java
    """

    def __init__(self, unit):
        self.count = 0
        self.reservoir = Reservoir(unit)

    def update(self, value):
        self.count += 1
        self.reservoir.update(value)

    def get_count(self):
        return self.count

    def get_snapshot(self):
        return self.reservoir.get_snapshot()

    def view(self, count=True, ty=True):
        result = self.get_snapshot().view()
        if count:
            result['count'] = self.get_count()
        if ty:
            result['type'] = 'histogram'
        return result
