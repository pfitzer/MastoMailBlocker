import time

import requests

from app.models import Domain


def initial_mail_adding(client) -> bool:
    """
    Adds initial email domains to the email domain block list for a specified client.

    Parameters:
    - client (Client): The client to add the email domains for.

    Returns:
    - bool: True if the domains were successfully added, False otherwise.
    """
    try:
        domains = Domain.objects.all()
        n = 1
        for domain in domains:
            # django api has a limit of 300 calls in 5 min
            if n >= 299:
                time.sleep(60 * 5)
            headers = {'Authorization': 'Bearer ' + client.access_token}
            payload = {'domain': domain}
            r = requests.post(f"{client.client_url}/api/v1/admin/email_domain_blocks", headers=headers,
                              data=payload)
            n += 1
            if r.status_code != 200:
                continue
    except Exception as e:
        return False

    return True