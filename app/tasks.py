import os
import time

from django.conf import settings

from app.exception import VerifyFailedException
from app.models import Domain
from django.core.management import call_command


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
            try:
                mastodon.send_domain_block(domain)
            except VerifyFailedException:
                break
            # django api has a limit of 300 calls in 5 min
            time.sleep(0.5)
    except Exception as e:
        return False

    return True


def create_db_backup():
    call_command('dumpdata', '>', os.path.join(settings.BASE_DIR, 'backup', 'backup.json'))
