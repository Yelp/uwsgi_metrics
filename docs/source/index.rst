.. uwsgi_metrics documentation master file, created by
   sphinx-quickstart on Fri May 13 14:16:02 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

uwsgi_metrics
*************

Overview
========

uwsgi_metrics is a port of Coda Hale's Metrics_ package to the uWSGI_ stack.
It allows you to use functions such as :py:func:`uwsgi_metrics.timing` to
gather application-level metrics::

        with timing(__name__, 'my_timer'):
            do_some_operation()

You can then invoke the :py:func:`uwsgi_metrics.view` function to get a
dictionary of metrics information::

        {
          "my_module_name": {
            "my_timer": {
              "type": "timer",
              "duration": {
                "p98": 1.4624929428100582,
                "p99": 1.6739368438720703,
                "p75": 0.4450678825378418,
                "p999": 1.6739368438720703,
                "min": 0.25391578674316406,
                "max": 1.6739368438720703,
                "p95": 0.92144012451171652,
                "std_dev": 0.21753626933399898,
                "mean": 0.45870650898326528,
                "median": 0.40006637573242188,
                "unit": "milliseconds"
              },
              "rate": {
                "m5": 2.0715749688040106e-53,
                "m1": 2.2285181292345502e-264,
                "m15": 3.6957346986808987e-18,
                "count": 88,
                "mean": 0.0024034510262515092,
                "unit": "seconds"
              }
            }
          }
        }

You can wire up :py:func:`uwsgi_metrics.view` to an HTTP endpoint so that you can
interactively monitor the performance of your production code.

Setup
=====

There are a couple of steps required before you can use uwsgi_metrics:

1. uWSGI must be started with a mule process;  this is done by passing the
   ``--mule`` option_ to the uWSGI executable.
2. The :py:func:`uwsgi_metrics.initialize` method must invoked in the master
   process prior to forking.

Performance
===========

It takes approximately 30us to log a metric on a 2.3GHz Xeon E5.  The
:py:func:`uwsgi_metrics.timing` context manager adds a further 20us, to give
a total of approximately 50us.

As a very rough guideline, you're probably not going to notice the overhead of
logging 10 metrics (0.5ms) during a service call, but you will start to notice the
overhead of logging 100 metrics (5ms).

API
===

.. currentmodule:: uwsgi_metrics

.. autofunction:: initialize

.. autofunction:: view

.. autofunction:: counter

.. autofunction:: histogram

.. autofunction:: meter

.. autofunction:: timer

.. autofunction:: timing(module, name)



.. _Metrics: http://metrics.codahale.com/
.. _uWSGI: http://uwsgi-docs.readthedocs.org/en/latest/
.. _option: http://uwsgi-docs.readthedocs.org/en/latest/Options.html#mule
