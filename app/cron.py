import urllib.request

import requests
from django.db import IntegrityError
from django_cron import CronJobBase, Schedule
from django.conf import settings

from app.models import Client, Domain


class DomainCronJob(CronJobBase):
    """
    DomainCronJob Class

    This class represents a domain cron job that is executed periodically to update the domain data and perform certain actions.

    Attributes:
        RUN_EVERY_MINS (int): The frequency (in minutes) at which the cron job should run.
        schedule (Schedule): The schedule object specifying the run frequency.
        code (str): The code identifier for the cron job.

    Methods:
        do(): Executes the cron job by fetching a list of domains, iterating through each domain, and performing certain actions.
    """
    RUN_EVERY_MINS = 120

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.domain_cron_job'

    def do(self):
        domains = urllib.request.urlopen(settings.DISPOSABLE_MAILS_URL)
        clients = Client.objects.all()
        for client in clients:
            for line in domains.readlines():
                try:
                    domain = Domain()
                    domain.name = line.decode('utf-8').strip()
                    domain.save()
                    headers = {'Authorization': 'Bearer ' + client.access_token}
                    payload = {'domain': domain.name}
                    r = requests.post(f"{client.client_url}/api/v1/admin/email_domain_blocks", headers=headers,
                                      data=payload)
                except Exception | IntegrityError:
                    continue
