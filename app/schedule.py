import time
import urllib.request

from django.conf import settings
from django.db import IntegrityError

from app.mastodon import Mastodon
from app.models import Client, Domain


def update_mail_domains():
    domains = urllib.request.urlopen(settings.DISPOSABLE_MAILS_URL)
    clients = Client.objects.all()
    for client in clients:
        mastodon = Mastodon(client)
        for line in domains.readlines():
            try:
                domain = Domain()
                domain.name = line.decode('utf-8').strip()
                domain.save()
                status_code = mastodon.send_domain_block(domain.name)
                time.sleep(1)
            except Exception:
                continue
            except IntegrityError:
                continue