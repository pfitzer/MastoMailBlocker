from django.template.defaulttags import register

from app.mastodon import Mastodon
from app.models import Domain, Client


@register.inclusion_tag("domain_count.html")
def show_domain_count():
    return {
        'domain_count': Domain.objects.all().count(),
        'client_count': Client.objects.all().count()
    }


@register.inclusion_tag("latest_instances.html")
def show_latest_instances():
    context = {'clients': []}
    clients = Client.objects.all().order_by('-created_at')[:3]
    for client in clients:
        mastodon = Mastodon(client)
        result = mastodon.get_instance()
        if result is not None:
            context['clients'].append(result)
    return context
