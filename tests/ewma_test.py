import testify as T

from uwsgi_metrics.ewma import EWMA

MAX_DIFFERENCE = 0.00000001


class EWMATest(T.TestCase):
    """Translated from EWMATest.java"""

    __test__ = False

    ewma = None
    expected_rates = None

    def elapse_minute(self, ewma):
        for i in xrange(12):
            ewma.tick()

    def assert_almost_equal(self, lval, rval, max_difference):
        T.assert_lte(abs(lval - rval), max_difference)

    def test_ewma(self):
        self.ewma.update(3)
        self.ewma.tick()
        for rate in self.expected_rates:
            self.assert_almost_equal(
                self.ewma.get_rate(), rate, MAX_DIFFERENCE)
            self.elapse_minute(self.ewma)


class OneMinuteEWMATest(EWMATest):

    ewma = EWMA.one_minute_EWMA()

    expected_rates = [
        0.6,
        0.22072766,
        0.08120117,
        0.02987224,
        0.01098938,
        0.00404277,
        0.00148725,
        0.00054713,
        0.00020128,
        0.00007405,
        0.00002724,
        0.00001002,
        0.00000369,
        0.00000136,
        0.00000050,
        0.00000018,
        ]


class FiveMinuteEWMATest(EWMATest):

    ewma = EWMA.five_minute_EWMA()

    expected_rates = [
        0.6,
        0.49123845,
        0.40219203,
        0.32928698,
        0.26959738,
        0.22072766,
        0.18071653,
        0.14795818,
        0.12113791,
        0.09917933,
        0.08120117,
        0.06648190,
        0.05443077,
        0.04456415,
        0.03648604,
        0.02987224
        ]


class FifteenMinuteEWMATest(EWMATest):

    ewma = EWMA.fifteen_minute_EWMA()

    expected_rates = [
        0.6,
        0.56130419,
        0.52510399,
        0.49123845,
        0.45955700,
        0.42991879,
        0.40219203,
        0.37625345,
        0.35198773,
        0.32928698,
        0.30805027,
        0.28818318,
        0.26959738,
        0.25221023,
        0.23594443,
        0.22072766,
        ]
