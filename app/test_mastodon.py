# File: test_mastodon.py
import unittest
from unittest.mock import MagicMock, patch, Mock
from urllib.parse import urlencode

from app.mastodon import Mastodon
from app.models import Client, Domain


class TestGetRedirectUrl(unittest.TestCase):
    def setUp(self):
        self.mastodon = Mastodon()
        self.mastodon.client = MagicMock()
        self.mastodon.client.pk = 1
        self.mock_req = Mock()
        self.mock_req.scheme = 'http'
        self.mock_req.META = {'HTTP_HOST': 'test.example.com'}

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

    @patch('requests.post')
    def test_register_app_success(self, mock_post):
        """Test register_app method on successful registration"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'client_id': 'test_client_id', 'client_secret': 'test_client_secret'}
        mock_post.return_value = mock_response

        client_id, client_secret = self.mastodon.register_app(self.mock_req)

        self.assertEqual(client_id, 'test_client_id')
        self.assertEqual(client_secret, 'test_client_secret')

    @patch('requests.post')
    def test_register_app_fail(self, mock_post):
        """Test register_app method on failed registration"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        client_id, client_secret = self.mastodon.register_app(self.mock_req)

        self.assertEqual(client_id, None)
        self.assertEqual(client_secret, None)

    def test_get_authorization_url(self):
        self.mastodon.get_redirect_url = Mock()
        self.mastodon.construct_api_url = Mock()
        self.mastodon.client.client_key = "test_client_key"
        self.mastodon.get_redirect_url.return_value = "http://localhost:8000/redirect"
        self.mastodon.construct_api_url.return_value = "http://localhost:8000/oauth/authorize/?"
        self.mastodon.SCOPES = "read write follow"

        request = "request"

        expected_payload = {
            'client_id': self.mastodon.client.client_key,
            'response_type': 'code',
            'grant_type': 'authorization_code',
            'redirect_uri': self.mastodon.get_redirect_url(request),
            'scope': self.mastodon.SCOPES
        }
        expected_url = self.mastodon.construct_api_url(self.mastodon.client.client_url,
                                                       '/oauth/authorize/?') + urlencode(expected_payload)

        result = self.mastodon.get_authorization_url(request)
        self.assertEqual(result, expected_url)
        self.mastodon.get_redirect_url.assert_called_with(request)
        self.mastodon.construct_api_url.assert_called_with(self.mastodon.client.client_url, '/oauth/authorize/?')
        self.assertEqual(2, self.mastodon.construct_api_url.call_count)
        self.assertEqual(2, self.mastodon.get_redirect_url.call_count)



if __name__ == '__main__':
    unittest.main()
