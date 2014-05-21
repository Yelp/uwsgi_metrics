from uwsgi_metrics.meter import Meter
from uwsgi_metrics.histogram import Histogram


class Timer(object):
    """A timer metric which aggregates timing durations and provides duration
    statistics, plus throughput statistics via a Meter.

    Translated from Timer.java
    """

    def __init__(self, unit):
        self.meter = Meter()
        self.histogram = Histogram(unit)

    def view(self):
        result = {
            'duration': self.histogram.view(count=False, ty=False),
            'rate': self.meter.view(ty=False),
            'type': 'timer',
            }
        return result

    def update(self, duration):
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
