from django.contrib import admin

from app.models import Client

admin.site.site_header = "MastoMailBlocker Admin"
admin.site.site_title = "MastoMailBlocker"
admin.site.index_title = "Welcome to MastoMailBlocker"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('client_url', 'created_at')
