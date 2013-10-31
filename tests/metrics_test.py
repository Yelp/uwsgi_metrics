import contextlib

import mock
import testify as T

import uwsgi_metrics


class MetricsTest(T.TestCase):

    def test(self):
        # mock.sentinel cannot be marshalled so let's roll our own
        timer_view_sentinel = 17
        histogram_view_sentinel = 18

        with mock.patch('os.getpid', return_value=42):
            # Return value matches mocked-out uwsgi.masterpid(), as defined in
            # uwsgi_metrics.metrics
            uwsgi_metrics.initialize()

        with contextlib.nested(
            mock.patch('uwsgi_metrics.metrics.Timer', autospec=True),
            mock.patch('uwsgi_metrics.metrics.Histogram', autospec=True),
                ) as (mock_timer, mock_histogram):
            mock_timer_instance = mock_timer.return_value
            mock_timer_instance.view.return_value = timer_view_sentinel

            mock_histogram_instance = mock_histogram.return_value
            mock_histogram_instance.view.return_value = histogram_view_sentinel

            with uwsgi_metrics.timer('foo'):
                pass

            # Any value will do here, just pick something
            uwsgi_metrics.histogram('bar', 27)

        uwsgi_metrics.metrics.periodically_write_metrics_to_mmaped_file(None)

        expected_view = {
            'timers': {
                'foo': timer_view_sentinel,
                },
            'histograms': {
                'bar': histogram_view_sentinel,
                }
            }

        T.assert_dicts_equal(uwsgi_metrics.view(), expected_view)
