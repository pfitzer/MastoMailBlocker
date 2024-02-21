import urllib.parse

import requests
from django_q.tasks import async_task

APP_NAME = "MastoMailBlocker"
SCOPES = 'read admin:write:email_domain_blocks'


class Mastodon:
    """
    class Mastodon:
    """

    def __init__(self, client=None):
        self.client = client

    def get_redirect_url(self, request):
        """
        Get the redirect URL for the client.

        Parameters:
        - self (instance): The instance of the class.
        - request (request): The HTTP request object.

        Returns:
        - str: The redirect URL formed using the request's scheme, HTTP host, and the client's primary key.

        Example:
        >>> client = Client.objects.get(pk=1)
        >>> request = HttpRequest()
        >>> request.scheme = 'https'
        >>> request.META = {'HTTP_HOST': 'example.com'}
        >>> redirect_url = get_redirect_url(client, request)
        >>> print(redirect_url)
        'https://example.com/get_code/1/'

        Note:
        - The primary key of the client is used to form the redirect URL.
        """
        return f'{request.scheme}://{request.META["HTTP_HOST"]}/get_code/{self.client.pk}/'

    def construct_api_url(self, base_url, endpoint):
        """
        Construct API url by combining base_url and endpoint.

        :param base_url: The base URL of the API.
        :type base_url: str
        :param endpoint: The endpoint of the API.
        :type endpoint: str
        :return: The constructed API url.
        :rtype: str
        """
        return f'{base_url}{endpoint}'

    def register_app(self, request):
        """
        Registers the application with the OAuth2 server.

        Args:
            self: The instance of the class calling the method.
            request: The HTTP request object.

        Returns:
            If the registration is successful (status code 200), returns a tuple containing the client id and client secret generated by the server.
            If the registration fails, returns None, None.
        """
        payload = {
            'client_name': APP_NAME,
            'redirect_uris': self.get_redirect_url(request),
            'scopes': SCOPES
        }
        req = requests.post(self.construct_api_url(self.client.client_url, '/api/v1/apps'), data=payload)
        if req.status_code == 200:
            response = req.json()
            client_id = response['client_id']
            client_secret = response['client_secret']
            return client_id, client_secret
        else:
            return None, None

    def get_authorization_url(self, request):
        """
        Get the authorization URL for the OAuth 2.0 flow.

        :param request: The current request object.
        :return: The authorization URL.

        The `get_authorization_url` method constructs an authorization URL for the OAuth 2.0 flow. It takes the `request` parameter, which is the current request object.

        The method first creates a payload dictionary containing the necessary parameters for the authorization URL, including the client ID, response type, grant type, redirect URI, and scope
        *. It then constructs the base API URL using the client URL and the specific path for the authorization endpoint.

        Finally, the method appends the payload to the URL by encoding it using the `url_encode` method from the `urllib.parse` module. The resulting URL is returned.

        Example usage:
            request = create_request_object()
            authorization_url = get_authorization_url(request)
        """
        payload = {
            'client_id': self.client.client_key,
            'response_type': 'code',
            'grant_type': 'authorization_code',
            'redirect_uri': self.get_redirect_url(request),
            'scope': SCOPES
        }
        url = self.construct_api_url(self.client.client_url, '/oauth/authorize/?')
        return url + urllib.parse.urlencode(payload)

    def obtain_access_token(self, code: str, request):
        """

        Obtains an access token from the OAuth provider.

        Parameters:
        - code (str): The authorization code received from the OAuth provider.
        - request (HttpRequest): The HTTP request object from the client.

        Returns:
        - str: The access token obtained from the OAuth provider.

        """
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client.client_key,
            'client_secret': self.client.client_secret,
            'redirect_uri': self.get_redirect_url(request),
            'scope': SCOPES
        }

        req = requests.post(self.construct_api_url(self.client.client_url, '/oauth/token'), data=payload)
        response = req.json()
        return response['access_token']

    def send_domain_block(self, domain: str):
        """
        Sends a domain block request to the API.

        Parameters:
        - domain (str): The domain to be blocked.

        Returns:
        - status_code (int): The HTTP status code received from the API.

        Example usage:
            send_domain_block('example.com')
        """
        headers = {'Authorization': 'Bearer ' + self.client.access_token}
        payload = {'domain': domain}
        r = requests.post(self.construct_api_url(self.client.client_url, '/api/v1/admin/email_domain_blocks'),
                          headers=headers,
                          data=payload)
        return r.status_code

    def verify_credentials(self):
        """
        Verifies the credentials of the client.

        :return: True if the credentials are valid, False otherwise
        """
        headers = {'Authorization': 'Bearer ' + self.client.access_token}
        r = requests.get(self.construct_api_url(self.client.client_url, '/api/v1/apps/verify_credentials'),
                         headers=headers)
        return r.status_code == 200

    def get_instance(self):
        r = requests.get(self.construct_api_url(self.client.client_url, '/api/v2/instance'))
        if r.status_code == 200:
            return r.json()
        return None

    def auth_ready(self):
        """
        This method is used to initiate the process of adding the initial mail in the application.

        :param self: The instance of the class.
        """
        if self.verify_credentials():
            async_task("app.tasks.initial_mail_adding", self)
        else:
            self.client.delete()
