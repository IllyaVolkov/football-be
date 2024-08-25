import unittest
from unittest.mock import patch, Mock
from crawler.crawlers.starwars import StarWarsCrawler


class TestBaseCrawler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_obj = Mock()
        cls.mock_obj.name = "test"
        cls.mock_obj.base_url = "https://example.com"
        cls.mock_obj.players_path = "/path"
        cls.mock_obj.pagination = "N"

        cls.crawler = StarWarsCrawler()

        cls.crawler.source = cls.mock_obj

    def test_init(self):
        self.assertEqual(self.crawler.source.name, "test")

    @patch("requests.get")
    def test_fetch_data_no_pagination_successful(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["result1", "result2"]
        mock_get.return_value = mock_response

        results, count = self.crawler.fetch_data()
        self.assertEqual(results, ["result1", "result2"])
        self.assertIsNone(count)

    @patch("requests.get")
    def test_fetch_data_no_pagination_fail(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.crawler.fetch_data()

        self.assertIn("Failed to fetch data", str(context.exception))

    @patch("requests.get")
    def test_fetch_data_pagination_limit_offset(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": ["result1", "result2"],
            "count": 2,
        }
        mock_get.return_value = mock_response

        self.crawler.source.pagination = "L"
        results, count = self.crawler.fetch_data(limit=1, offset=1)
        self.assertEqual(results, ["result1", "result2"])
        self.assertEqual(count, 2)

    @patch("requests.get")
    def test_fetch_data_pagination_page_number(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": ["result1", "result2"],
            "count": 2,
            "next": "next_page_url",
        }
        mock_get.return_value = mock_response

        self.crawler.source.pagination = "P"
        results, count, next = self.crawler.fetch_data(page=1)
        self.assertEqual(results, ["result1", "result2"])
        self.assertEqual(count, 2)
        self.assertEqual(next, "next_page_url")
