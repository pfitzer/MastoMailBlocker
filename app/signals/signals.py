import django.dispatch
from django.dispatch import receiver

from app.utils import initial_mail_adding

client_initial = django.dispatch.Signal()


@receiver(client_initial)
def send_domains(sender, instance, **kwargs):
    initial_mail_adding(instance)