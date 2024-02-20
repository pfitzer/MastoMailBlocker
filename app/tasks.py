import time

from app.models import Domain


def initial_mail_adding(mastodon) -> bool:
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
            status_code = mastodon.send_domain_block(domain)
            # django api has a limit of 300 calls in 5 min
            time.sleep(1)
            if status_code != 200:
                continue
    except Exception as e:
        return False

    return True
