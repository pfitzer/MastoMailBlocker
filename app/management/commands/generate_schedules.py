from django.core.management import BaseCommand
from django_q.models import Schedule


class Command(BaseCommand):
    """

    This class represents a command that generates schedules for MastoMailBlocker.

    Attributes:
        help (str): A brief description of the command's purpose.

    Methods:
        handle(*args, **options): Executes the logic of the command.

    """
    help = 'Generates schedules for MastoMailBlocker'

    def handle(self, *args, **options):
        Schedule.objects.all().delete()
        Schedule.objects.create(
            func='app.schedule.update_mail_domains',
            schedule_type=Schedule.WEEKLY,
            repeats=-1)
