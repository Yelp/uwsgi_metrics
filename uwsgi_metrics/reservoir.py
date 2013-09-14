import math
import random
import time

import treap

from uwsgi_metrics.snapshot import Snapshot


DEFAULT_SIZE = 1028

DEFAULT_ALPHA = 0.015

RESCALE_THRESHOLD_S = 60 * 60


class Reservoir(object):
    """An exponentially decaying reservoir.

    Code cargo-culted from
    https://github.com/codahale/metrics/blob/master/metrics-core/src/main/java/com/codahale/metrics/ExponentiallyDecayingReservoir.java
    """

    def __init__(self, size=DEFAULT_SIZE, alpha=DEFAULT_ALPHA):
        self.size = size
        self.alpha = alpha
        self.start_time = self.current_time_in_seconds()
        self.next_scale_time = self.start_time + RESCALE_THRESHOLD_S
        self.values = treap.treap()

    def current_time_in_seconds(self):
        return time.time()

    def first_key(self):
        return self.values.find_min()

    def weight(self, t):
        return math.exp(self.alpha * t)

    def update(self, value, timestamp=None):
        if timestamp is None:
            timestamp = self.current_time_in_seconds()
        self.rescale_if_needed()
        priority = self.weight(timestamp - self.start_time) / random.random()
        if len(self.values) < self.size:
            self.values[priority] = value
        else:
            first = self.first_key()
            if first < priority and not priority in self.values:
                del self.values[first]
                self.values[priority] = value

    def rescale_if_needed(self):
        now = self.current_time_in_seconds()
        next_ = self.next_scale_time
        if now >= next_:
            self.rescale(now, next_)

    def rescale(self, now, next_):
        old_start_time = self.start_time
        self.start_time = self.current_time_in_seconds()
        self.next_scale_time = now + RESCALE_THRESHOLD_S
        new_values = treap.treap()
        for key in self.values.keys():
            new_key = key * math.exp(
                -self.alpha * (self.start_time - old_start_time))
            new_values[new_key] = self.values[key]
        self.values = new_values

    def snapshot(self):
        return Snapshot(sorted(self.values.values()))
