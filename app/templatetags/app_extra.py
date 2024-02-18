from django.template.defaulttags import register

from app.models import Domain


@register.inclusion_tag("domain_count.html")
def show_domain_count():
    domains = Domain.objects.all().count()
    return {
        'count': domains
    }