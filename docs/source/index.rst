.. uwsgi_metrics documentation master file, created by
   sphinx-quickstart on Fri May 13 14:16:02 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

uwsgi_metrics
*************

What is uwsgi_metrics?
======================

uwsgi_metrics is a port of Coda Hale's Metrics_ package to the uWSGI_
stack.  In a nutshell, it allows you to use functions such as
:py:func:`uwsgi_metrics.timing` to time sections of code::

        from uwsgi_metrics import timing
        with timing('my_timer'):
            do_some_operation()

and then invoke the :py:func:`uwsgi_metrics.view` function to get a dictionary
of metrics information::

        {
          "timers": {
            "my_timer": {
              "duration": {
                "p98": 0.0014624929428100582,
                "p99": 0.0016739368438720703,
                "p75": 0.0004450678825378418,
                "p99.9": 0.0016739368438720703,
                "min": 0.00025391578674316406,
                "max": 0.0016739368438720703,
                "p95": 0.00092144012451171652,
                "stddev": 0.00021753626933399898,
                "mean": 0.00045870650898326528,
                "p50": 0.00040006637573242188,
                "count": 88
              },
              "throughput": {
                "m5": 2.0715749688040106e-53,
                "m1": 2.2285181292345502e-264,
                "m15": 3.6957346986808987e-18,
                "count": 88,
                "mean": 0.0024034510262515092
              }
            }
          }
        }

You can wire up :py:func:`uwsgi_metrics.view` to an HTTP endpoint so that you can
interactively monitor the performance of your production code.

How do I use uwsgi_metrics?
===========================

There are a couple of steps required before you can use uwsgi_metrics:

1. uWSGI must be started with a mule process;  this is done by passing the
   ``--mule`` option to the uWSGI executable.
2. The :py:func:``uwsgi_metrics.initialize`` method must invoked in the master
   process prior to forking.

How fast is uwsgi_metrics?
==========================

It takes approximately 30us to log a metric on a 2.3GHz Xeon E5.  The
:py:func:`uwsgi_metrics.timer` context manager adds a further 20us, to give
a total of approximately 50us.

As a very rough guideline, you're probably not going to notice the overhead of
logging 10 metrics (0.5ms) during a service call, but you will start to notice the
overhead of logging 100 metrics (5ms).

What is the architecture?
=========================

Assume that we're running with the following three types of uWSGI processes:

* One master process
* One mule process
* One or more worker processes

Worker processes send metrics updates to the mule process e.g. using the
:py:func:`uwsgi_metrics.timer` context manager.  The mule process aggregates
these updates and periodically publishes them to an mmap'ed buffer using
the ``periodically_write_metrics_to_mmaped_buffer()`` function. Worker
processes can view the aggregated metrics from the mmap'ed buffer using the
:py:func:`uwsgi_metrics.view` function e.g. for publishing to an endpoint.

API
===

.. currentmodule:: uwsgi_metrics

.. autofunction:: initialize

.. autofunction:: view

.. autofunction:: timer

.. autofunction:: timing(name)

.. autofunction:: histogram


.. _Metrics: http://metrics.codahale.com/
.. _uWSGI: http://uwsgi-docs.readthedocs.org/en/latest/
