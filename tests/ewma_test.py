"""Translated from EWMATest.java"""


from uwsgi_metrics.ewma import EWMA


def assert_ewma(ewma, expected_rates):
    max_difference = 0.00000001

    def elapse_minute(ewma):
        for i in xrange(12):
            ewma.tick()

    ewma.update(3)
    ewma.tick()
    for rate in expected_rates:
        assert abs(ewma.get_rate() - rate) < max_difference
        elapse_minute(ewma)


def test_one_minute_EWMA():
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

    ewma = EWMA.one_minute_EWMA()
    assert_ewma(ewma, expected_rates)


def test_five_minute_EWMA():
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

    ewma = EWMA.five_minute_EWMA()
    assert_ewma(ewma, expected_rates)


def test_fifteen_minute_EWMA():
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

    ewma = EWMA.fifteen_minute_EWMA()
    assert_ewma(ewma, expected_rates)
