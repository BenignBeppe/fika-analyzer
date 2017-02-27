from unittest import TestCase
from unittest.mock import patch

import fika_analyzer


class FikaAnalyzerTests(TestCase):
    def test_get_pageviews(self):
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
                project="www.wiki.org",
                page="Test",
                start_date="20161209",
                end_date="20161210"
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

    def test_send_pageview_request_for_page_with_slash(self):
        with patch("requests.get") as mock_get:
            fika_analyzer.send_pageview_request(
                project="www.wiki.org",
                access="all-access",
                agent="user",
                page="Page/subpage",
                granularity="daily",
                start_date="20161209",
                end_date="20161209"
            )
            expected_url = "https://wikimedia.org/api/rest_v1/metrics/" \
                           "pageviews/per-article/www.wiki.org/all-access/" \
                           "user/Page%2Fsubpage/daily/20161209/20161209"
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

    def test_get_number_of_invitees(self):
        with patch("fika_analyzer.send_category_request") as \
             mock_send_category_request:
            mock_response = {
                "query": {
                    "pages": {
                        "123": {
                            "categoryinfo": {"pages": 7}
                        }
                    }
                }
            }
            mock_send_category_request.return_value = mock_response
            result = fika_analyzer.get_number_of_invitees()
            self.assertEqual(7, result)

    def test_send_category_request(self):
        with patch("requests.get") as mock_get:
            fika_analyzer.send_category_request(
                api_url="https://www.wiki.org/w/api.php",
                category="Category"
            )
            mock_get.assert_called_once_with(
                url="https://www.wiki.org/w/api.php",
                params={
                    "action": "query",
                    "format": "json",
                    "prop": "categoryinfo",
                    "titles": "Category"
                }
            )
