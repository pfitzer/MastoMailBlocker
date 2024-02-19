from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Client
from app.utils import initial_mail_adding


@receiver(post_save, sender=Client)
def send_domains(sender, instance, created, **kwargs):
    initial_mail_adding(instance)