from django.contrib import admin

from app.models import Client, Domain, Faq

admin.site.site_header = "MastoMailBlocker Admin"
admin.site.site_title = "MastoMailBlocker"
admin.site.index_title = "Welcome to MastoMailBlocker"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_url', 'created_at')


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')
    list_filter = ['published']
    actions = ['make_published', 'make_unpublished']

    @admin.action(description="Mark selected FAQs as published")
    def make_published(self, request, queryset):
        queryset.update(published=True)

    @admin.action(description="Mark selected FAQs as unpublished")
    def make_unpublished(self, request, queryset):
        queryset.update(published=False)