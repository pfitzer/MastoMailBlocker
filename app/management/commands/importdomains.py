import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from app.models import Domain


class Command(BaseCommand):
    help = 'Import email domains to database'

    def handle(self, *args, **options):
        self.stdout.write("Importing disposable domains...")
        domains = urllib.request.urlopen(settings.DISPOSABLE_MAILS_URL)
        for line in domains.readlines():
            try:
                domain = Domain()
                domain.name = line.decode('utf-8').strip()
                domain.save()
            except IntegrityError as e:
                continue
            except AttributeError:
                self.stdout.write(self.style.ERROR('Error importing "%s"' % line))
                continue
        self.stdout.write(
            self.style.SUCCESS('Successfully imported domains')
        )
