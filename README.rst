|build-status| |docs|

uwsgi_metrics
=============

Overview
--------

uwsgi_metrics is a port of Coda Hale's Metrics_ package to the uWSGI_ stack.
It allows you to use functions such as :py:func:`uwsgi_metrics.timing` to
gather application-level metrics:

.. code:: Python

        with timing(__name__, 'my_timer'):
            do_some_operation()

You can then invoke the :py:func:`uwsgi_metrics.view` function to get a
dictionary of metrics information::


.. code:: JSON

        {
          "version": "1.1.1",
          "counters": {},
          "gauges": {},
          "histograms": {},
          "meters": {},
          "timers": {
            "my_module.my_timer": {
              "count": 22,
              "p98": 4.8198699951171875,
              "m15_rate": 1.0033118138834103,
              "p75": 1.9915103912353516,
              "p99": 4.8198699951171875,
              "min": 1.4159679412841797,
              "max": 4.8198699951171875,
              "m5_rate": 1.0098078505715211,
              "p95": 4.7961950302124023,
              "m1_rate": 1.0454161929696191,
              "duration_units": "milliseconds",
              "stddev": 0.92399302814991413,
              "mean_rate": 1.2074971885928811,
              "rate_units": "calls/second",
              "p999": 4.8198699951171875,
              "p50": 1.649022102355957,
              "mean": 1.9796761599454014
            }
          }
        }

You can wire up :py:func:`uwsgi_metrics.view` to an HTTP endpoint so that you can
interactively monitor the performance of your production code.

Setup
-----

There are a couple of steps required before you can use uwsgi_metrics:

1. uWSGI must be started with a mule process;  this is done by passing the
   ``--mule`` option_ to the uWSGI executable.
2. The :py:func:`uwsgi_metrics.initialize` method must invoked in the master
   process prior to forking.

Performance
-----------

It takes approximately 30us to log a metric on a 2.3GHz Xeon E5.  The
:py:func:`uwsgi_metrics.timing` context manager adds a further 20us, to give
a total of approximately 50us.

As a very rough guideline, you're probably not going to notice the overhead of
logging 10 metrics (0.5ms) during a service call, but you will start to notice the
overhead of logging 100 metrics (5ms).

Documentation
-------------

More documentation is available at http://uwsgi-metrics.readthedocs.org

License
-------

Copyright (c) 2010-2015 Coda Hale, Yammer.com

Copyright (c) 2015, Yelp, Inc.

Published under Apache Software License 2.0, see LICENSE

.. |build-status| image:: https://travis-ci.org/Yelp/uwsgi_metrics.png?branch=master
    :alt: Build Status
    :scale: 100%
    :target: https://travis-ci.org/Yelp/uwsgi_metrics?branch=master

.. |docs| image:: https://readthedocs.org/projects/uwsgi-metrics/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/uwsgi-metrics/?badge=latest

.. _Metrics: http://metrics.codahale.com/
.. _uWSGI: http://uwsgi-docs.readthedocs.org/en/latest/
.. _option: http://uwsgi-docs.readthedocs.org/en/latest/Options.html#mule
