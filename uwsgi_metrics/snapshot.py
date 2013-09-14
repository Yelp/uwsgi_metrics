class Snapshot(object):
    """A snapshot of a reservoir state."""

    def __init__(self, values):
        self.values = values

    def get_value(self, quantile):
        if quantile < 0.0 or quantile > 1.0:
            raise ValueError(quantile + " is not in [0..1]")

        if len(self.values) == 0:
            return 0.0

        pos = quantile * len(self.values) + 1

        if pos < 1:
            return self.values[0]

        if pos >= len(self.values):
            return self.values[len(self.values) - 1]

        lower = self.values[int(pos) - 1]
        upper = self.values[int(pos)]
        return lower + (pos - math.floor(pos)) * (upper - lower);

    def get_median(self):
        return self.get_value(0.5)

    def get_75th_percentile(self):
        return self.get_value(0.75)

    def get_95th_percentile(self):
        return self.get_value(0.95)

    def get_98th_percentile(self):
        return self.get_value(0.98)

    def get_99th_percentile(self):
        return self.get_value(0.99)

    def get_999th_percentile(self):
        return self.get_value(0.999)

    def get_mean(self):
        if len(self.values) == 0:
            return 0.0
        return sum(self.values) / len(self.values)

    def size(self):
        return len(self.values)
