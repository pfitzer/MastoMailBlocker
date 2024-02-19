from django.template.defaulttags import register

from app.models import Domain, Client


@register.inclusion_tag("domain_count.html")
def show_domain_count():
    return {
        'domain_count': Domain.objects.all().count(),
        'client_count': Client.objects.all().count()
    }