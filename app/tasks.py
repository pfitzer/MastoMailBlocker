import os
import time
from datetime import datetime

from django.conf import settings
from django.core.management import call_command

BACKUP_DIR = os.path.join(settings.BASE_DIR, 'backup')
DAYS = 7


def initial_mail_adding(mastodon, domains) -> bool:
    """
    Adds initial email domains to the email domain block list for a specified client.

    Parameters:
    - client (Client): The client to add the email domains for.

    Returns:
    - bool: True if the domains were successfully added, False otherwise.
    """
    try:
        for domain in domains:
            req = mastodon.send_domain_block(domain)
            # django api has a limit of 300 calls in 5 min
            if int(req['remaining']) <= 10:
                time.sleep(300)
    except Exception as e:
        return False

    return True


def create_db_backup() -> int:
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
    backup_file = os.path.join(BACKUP_DIR, f'backup-{date}.json')
    with open(backup_file, 'w') as f:
        call_command('dumpdata', stdout=f)
    f.close()

    delete_old_backups()
    return 0


def delete_old_backups():
    """
    Deletes old backups from the designated backup directory.

    :return: None
    """
    for root, dirs, files in os.walk(BACKUP_DIR):
        for name in files:
            filename = os.path.join(root, name)
            if os.stat(filename).st_mtime < time.time() - (DAYS * 86400):
                os.remove(filename)
