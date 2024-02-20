# File: test_mastodon.py
import unittest
from unittest.mock import MagicMock, patch
from app.mastodon import Mastodon


class TestGetRedirectUrl(unittest.TestCase):
    def setUp(self):
        self.mastodon = Mastodon()
        self.mastodon.client = MagicMock()
        self.mastodon.client.pk = 1

    def test_get_redirect_url(self):
        request = MagicMock()
        request.scheme = 'https'
        request.META = {'HTTP_HOST': 'example.com'}

        expected_result = 'https://example.com/get_code/1/'
        result = self.mastodon.get_redirect_url(request)

        self.assertEqual(expected_result, result)

    def test_base_url_and_endpoint(self):
        base_url = "http://api.example.com"
        endpoint = "/v1/project/"
        expected_url = "http://api.example.com/v1/project/"
        result_url = self.mastodon.construct_api_url(base_url, endpoint)
        self.assertEqual(result_url, expected_url, f"[Test Case] Received: {result_url}, Expected: {expected_url}")

    def test_missed_trailing_slash(self):
        base_url = "http://api.example.com"
        endpoint = "/v1/project/"
        expected_url = "http://api.example.com/v1/project/"
        result_url = self.mastodon.construct_api_url(base_url, endpoint)
        self.assertEqual(result_url, expected_url, f"[Test Case] Received: {result_url}, Expected: {expected_url}")

    def test_no_base_url(self):
        base_url = ""
        endpoint = "/v1/project/"
        expected_url = "/v1/project/"
        result_url = self.mastodon.construct_api_url(base_url, endpoint)
        self.assertEqual(result_url, expected_url, f"[Test Case] Received: {result_url}, Expected: {expected_url}")

    def test_no_endpoint(self):
        base_url = "http://api.example.com"
        endpoint = ""
        expected_url = "http://api.example.com"
        result_url = self.mastodon.construct_api_url(base_url, endpoint)
        self.assertEqual(result_url, expected_url, f"[Test Case] Received: {result_url}, Expected: {expected_url}")


if __name__ == '__main__':
    unittest.main()
