import urllib.parse

import requests

CLIENT_ID = 'mmA99Udahrs5XMtI_PIWRk5bibGMyu9KKSfy9V0gVSI'
CLIENT_SECRET = 'lucHNHmeyhaRsk80UMyaMUmzP2OMzXIlWyfsz-kKu2M'
CODE = 'a2Cr_rKmmAaN6kTykdPnDghUr0W4a2HClCLTLUhIe4g'
ACCESS_TOKEN = '3A-dSHgF473sIpfBhwqpeu9JTR-Z7qVwD2zURe4vSSM'


def register_app():
    payload = {
        'client_name': 'MastoMailBlocker',
        'redirect_uris': 'urn:ietf:wg:oauth:2.0:oob',
        'scopes': 'admin:write:email_domain_blocks'
    }
    req = requests.post('https://social.main-angler.de/api/v1/apps', data=payload)
    if req.status_code == 200:
        response = req.json()
        client_id = response['client_id']
        client_secret = response['client_secret']
        return client_id, client_secret
    else:
        return None, None


def verify_app():
    headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN
    }
    req = requests.get('https://social.main-angler.de/api/v1/apps/verify_credentials', headers=headers)
    response = req.json()
    foo = 'bar'

def authorization_code():
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'grant_type': 'authorization_code',
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'scope': 'admin:write:email_domain_blocks'
    }
    url = 'https://social.main-angler.de/oauth/authorize/?'
    print(url + urllib.parse.urlencode(payload))

def obtain_access_token():
    payload = {
        'grant_type': 'authorization_code',
        'code': CODE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        'scope': 'admin:write:email_domain_blocks'
    }

    req = requests.post('https://social.main-angler.de/oauth/token', data=payload)
    response = req.json()
    foo = 'bar'


if __name__ == '__main__':
    verify_app()
