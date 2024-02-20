import urllib.request

from django.conf import settings
from django.db import IntegrityError

from app.exception import VerifyFailedException
from app.mastodon import Mastodon
from app.models import Client, Domain


def update_mail_domains():
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
            try:
                mastodon = Mastodon(client)
                mastodon.send_domain_block(domain.name)
            except VerifyFailedException:
                break
