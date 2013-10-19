from uwsgi_metrics.meter import Meter
from uwsgi_metrics.histogram import Histogram


class Timer(object):
    """A timer metric which aggregates timing durations and provides duration
    statistics, plus throughput statistics via a Meter.

    Translated from Timer.java
    """

    def __init__(self, meter=None, histogram=None):
        self.meter = meter or Meter()
        self.histogram = histogram or Histogram()

    def update(self, duration=1):
        """Add a recorded duration."""
        if duration >= 0:
            self.histogram.update(duration)
            self.meter.mark()

    def get_count(self):
        return self.histogram.get_count()

    def get_fifteen_minute_rate(self):
        return self.meter.get_fifteen_minute_rate()

    def get_five_minute_rate(self):
        return self.meter.get_five_minute_rate()

    def get_one_minute_rate(self):
        return self.meter.get_one_minute_rate()

    def get_mean_rate(self):
        return self.meter.get_mean_rate()

    def get_snapshot(self):
        return self.histogram.get_snapshot()
