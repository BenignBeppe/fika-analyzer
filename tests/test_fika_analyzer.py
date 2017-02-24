from unittest import TestCase
from unittest.mock import patch

import fika_analyzer


class FikaAnalyzerTests(TestCase):
    def test_get_pageviews(self):
        project = "www.wiki.org"
        page = "Test"
        start_date = "20161209"
        end_date = "20161210"
        with patch("fika_analyzer.send_pageview_request") as \
             mock_send_pageview_request:
            mock_response = {
                "items": [
                    {"views": 8},
                    {"views": 4},
                ]
            }
            mock_send_pageview_request.return_value = mock_response
            result = fika_analyzer.get_pageviews(
                project,
                page,
                start_date,
                end_date
            )
            self.assertEqual(12, result)

    def test_send_pageview_request(self):
        with patch("requests.get") as mock_get:
            fika_analyzer.send_pageview_request(
                project="www.wiki.org",
                access="all-access",
                agent="user",
                page="Page",
                granularity="daily",
                start_date="20161209",
                end_date="20161209"
            )
            expected_url = "https://wikimedia.org/api/rest_v1/metrics/" \
                           "pageviews/per-article/www.wiki.org/all-access/" \
                           "user/Page/daily/20161209/20161209"
            mock_get.assert_called_once_with(expected_url)

    def test_get_number_of_questions(self):
        with patch("fika_analyzer.send_sections_request") as \
             mock_send_sections_request:
            mock_response = {
                "parse": {
                    "sections": [
                        {"level": "1"},
                        {"level": "2"},
                        {"level": "3"},
                        {"level": "2"},
                        {"level": "2"}
                    ]
                }
            }
            mock_send_sections_request.return_value = mock_response
            result = fika_analyzer.get_number_of_questions()
            self.assertEqual(3, result)

    def test_send_sections_request(self):
        with patch("requests.get") as mock_get:
            fika_analyzer.send_sections_request(
                api_url="https://www.wiki.org/w/api.php",
                page="Page"
            )
            mock_get.assert_called_once_with(
                url="https://www.wiki.org/w/api.php",
                params={
                    "action": "parse",
                    "format": "json",
                    "page": "Page",
                    "prop": "sections"
                }
            )
