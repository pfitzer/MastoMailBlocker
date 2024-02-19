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
        for domain in domains:
            headers = {'Authorization': 'Bearer ' + client.access_token}
            payload = {'domain': domain}
            r = requests.post(f"{client.client_url}/api/v1/admin/email_domain_blocks", headers=headers,
                              data=payload)
            if r.status_code != 200:
                continue
    except Exception as e:
        return False

    return True