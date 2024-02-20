import urllib.parse

import requests
from django_q.tasks import async_task

from app.exception import VerifyFailedException

APP_NAME = "MastoMailBlocker"
SCOPES = 'read admin:write:email_domain_blocks'


class Mastodon:
    """
    Class Mastodon

    A class for interacting with the Mastodon API.

    Attributes:
        client (Client): An instance of the Client class.

    Methods:
        __init__(client: Client = None):
            Initializes a Mastodon instance with an optional client.

        register_app():
            Registers the application with the Mastodon API and returns the client ID and secret.

        get_authorization_url(request, client_key: str):
            Generates the authorization URL for the Mastodon API based on the provided request and client key.

        obtain_access_token(code: str):
            Obtains an access token from the Mastodon API using the provided authorization code.

    """

    def __init__(self, client=None):
        self.client = client

    def register_app(self, request):
        payload = {
            'client_name': APP_NAME,
            'redirect_uris': f'{request.scheme}://{request.META["HTTP_HOST"]}/get_code/{self.client.pk}/',
            'scopes': SCOPES
        }
        req = requests.post(f'{self.client.client_url}/api/v1/apps', data=payload)
        if req.status_code == 200:
            response = req.json()
            client_id = response['client_id']
            client_secret = response['client_secret']
            return client_id, client_secret
        else:
            return None, None

    def get_authorization_url(self, request):
        payload = {
            'client_id': self.client.client_key,
            'response_type': 'code',
            'grant_type': 'authorization_code',
            'redirect_uri': f'{request.scheme}://{request.META["HTTP_HOST"]}/get_code/{self.client.pk}/',
            'scope': SCOPES
        }
        url = f'{self.client.client_url}/oauth/authorize/?'
        return url + urllib.parse.urlencode(payload)

    def obtain_access_token(self, code: str, request):
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client.client_key,
            'client_secret': self.client.client_secret,
            'redirect_uri': f'{request.scheme}://{request.META["HTTP_HOST"]}/get_code/{self.client.pk}/',
            'scope': SCOPES
        }

        req = requests.post(f'{self.client.client_url}/oauth/token', data=payload)
        response = req.json()
        return response['access_token']

    def send_domain_block(self, domain: str):
        if not self.verify_credentials():
            self.client.delete()
            raise VerifyFailedException('Invalid credentials')
        headers = {'Authorization': 'Bearer ' + self.client.access_token}
        payload = {'domain': domain}
        r = requests.post(f"{self.client.client_url}/api/v1/admin/email_domain_blocks", headers=headers,
                          data=payload)
        return r.status_code

    def verify_credentials(self):
        headers = {'Authorization': 'Bearer ' + self.client.access_token}
        r = requests.get(f'{self.client.client_url}/api/v1/apps/verify_credentials', headers=headers)
        return r.status_code == 200

    def auth_ready(self):
        async_task("app.tasks.initial_mail_adding", self)
