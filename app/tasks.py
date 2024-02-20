import os
import time
from datetime import datetime

from django.conf import settings
from django.core.management import call_command

from app.exception import VerifyFailedException
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
            try:
                mastodon.send_domain_block(domain)
            except VerifyFailedException:
                break
            # django api has a limit of 300 calls in 5 min
            time.sleep(0.5)
    except Exception as e:
        return False

    return True


def create_db_backup() -> None:
    """
    Create a backup of the database.

    This method creates a backup of the database by using the `dumpdata` command
    provided by Django. The backup file is saved in the 'backup' directory,
    located in the project's base directory. The file name is generated based
    on the current date and time.

    Returns:
        None

    Example usage:
        create_db_backup()
    """
    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = os.path.join(settings.BASE_DIR, 'backup', f'backup-{date}.json')
    with open(backup_file, 'w') as f:
        call_command('dumpdata', stdout=f)
    f.close()
