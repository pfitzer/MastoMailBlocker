import urllib.request

from django.conf import settings
from django.db import IntegrityError

from app.exception import MastodonException
from app.mastodon import Mastodon
from app.models import Client, Domain


def update_mail_domains():
    """

    This method updates the mail domains by retrieving a list of disposable mail domains from a specified URL and adding them to the database. It then iterates through all clients in the
    * database and for each client, it checks if it can connect to a Mastodon instance using the client's credentials. If successful, it sends a domain block request to the Mastodon instance
    * with the newly added domain. If verification fails, it deletes the client from the database and stops the iteration.

    """
    domains = urllib.request.urlopen(settings.DISPOSABLE_MAILS_URL)
    clients = Client.objects.all()
    for line in domains.readlines():
        try:
            domain = Domain();
            domain.name = line.decode('utf-8').strip()
            domain.save()
        except IntegrityError:
            continue
        for client in clients:
            mastodon = Mastodon(client)
            if mastodon.verify_credentials():
                mastodon.send_domain_block(domain.name)
            else:
                mastodon.client.delete()
                break
