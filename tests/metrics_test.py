import contextlib

import mock
import testify as T

import uwsgi_metrics


class MetricsTest(T.TestCase):

    def test(self):
        # mock.sentinel cannot be marshalled so let's roll our own
        timer_view_sentinel = 17
        histogram_view_sentinel = 18

        with contextlib.nested(
            mock.patch('uwsgi_metrics.metrics.Timer', autospec=True),
            mock.patch('uwsgi_metrics.metrics.Histogram', autospec=True),
                ) as (mock_timer, mock_histogram):
            mock_timer_instance = mock_timer.return_value
            mock_timer_instance.view.return_value = timer_view_sentinel

            mock_histogram_instance = mock_histogram.return_value
            mock_histogram_instance.view.return_value = histogram_view_sentinel

            with uwsgi_metrics.timing('foo'):
                pass

            # Any values will do here, just pick something
            uwsgi_metrics.timer('bar', 39)
            uwsgi_metrics.histogram('baz', 27)

        uwsgi_metrics.metrics.periodically_write_metrics_to_mmaped_buffer(None)

        expected_view = {
            'timers': {
                'foo': timer_view_sentinel,
                'bar': timer_view_sentinel,
                },
            'histograms': {
                'baz': histogram_view_sentinel,
                }
            }

        T.assert_dicts_equal(uwsgi_metrics.view(), expected_view)
