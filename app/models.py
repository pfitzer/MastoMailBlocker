from django.db import models


class Client(models.Model):
    client_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
    client_secret = models.CharField(max_length=255, unique=True, null=False, blank=False)
    client_url = models.CharField(max_length=255, unique=True, null=False, blank=False)
    client_code = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.client_url
