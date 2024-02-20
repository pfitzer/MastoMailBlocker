from urllib.parse import urlencode

import requests

APP_NAME = "MastoMailBlocker"
SCOPES = 'read admin:write:email_domain_blocks'


class Mastodon:
    def __init__(self, client=None):
        self.client = client

    def register_app(self, request):
        payload = self.build_payload('client_name', APP_NAME,
                                     'redirect_uris', self.get_redirect_uri(request),
                                     'scopes', SCOPES)

        return self.send_request('post', 'api/v1/apps', payload)

    def get_authorization_url(self, request):
        payload = self.build_payload('client_id', self.client.client_key,
                                     'response_type', 'code',
                                     'grant_type', 'authorization_code',
                                     'redirect_uri', self.get_redirect_uri(request),
                                     'scope', SCOPES)

        return self.get_client_url('oauth/authorize') + '?' + urlencode(payload)

    def obtain_access_token(self, code, request):
        payload = self.build_payload('grant_type', 'authorization_code',
                                     'code', code,
                                     'client_id', self.client.client_key,
                                     'client_secret', self.client.client_secret,
                                     'redirect_uri', self.get_redirect_uri(request),
                                     'scope', SCOPES)

        return self.send_request('post', 'oauth/token', payload)['access_token']

    def get_redirect_uri(self, request):
        return f'{request.scheme}://{request.META["HTTP_HOST"]}/get_code/{self.client.pk}/'

    def build_payload(self, *args):
        return {args[i]: args[i + 1] for i in range(0, len(args), 2)}

    def get_client_url(self, endpoint=''):
        return f'{self.client.client_url}/{endpoint}'

    def send_request(self, method, endpoint, payload=None, headers=None):
        response = getattr(requests, method)(self.get_client_url(endpoint), data=payload, headers=headers)
        if response.status_code != 200:
            response.raise_for_status()
        return response.json()
