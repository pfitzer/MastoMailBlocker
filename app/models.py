from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class ClientManager(models.Manager):
    """Custom manager for Client model."""

    def active(self):
        """Return only active clients."""
        return self.filter(is_active=True)

    def authenticated(self):
        """Return only clients with access tokens."""
        return self.exclude(access_token='')

    def ready_for_sync(self):
        """Return clients ready for domain sync."""
        return self.filter(
            is_active=True
        ).exclude(
            access_token=''
        )


class Client(models.Model):
    """
    Represents a Mastodon instance OAuth client.

    Handles OAuth credentials for automated domain blocking on Mastodon instances.

    OAuth Flow:
    1. Client created with only client_url
    2. App registration populates client_key and client_secret
    3. OAuth callback populates access_token
    """

    client_key = models.CharField(
        _("Client Key"),
        max_length=255,
        unique=True,
        blank=True,
        default='',
        help_text=_("OAuth client ID from Mastodon instance")
    )

    client_secret = models.CharField(
        _("Client Secret"),
        max_length=255,
        blank=True,
        default='',
        help_text=_("OAuth client secret (should be encrypted in production)")
    )

    client_url = models.URLField(
        _("Instance URL"),
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_("Base URL of the Mastodon instance")
    )

    access_token = models.CharField(
        _("Access Token"),
        max_length=500,
        blank=True,
        default='',
        help_text=_("OAuth access token - obtained after authorization")
    )

    is_active = models.BooleanField(
        _("Active"),
        default=True,
        db_index=True,
        help_text=_("Whether this client is actively syncing")
    )

    last_verified = models.DateTimeField(
        _("Last Verified"),
        null=True,
        blank=True,
        help_text=_("Last successful credential verification")
    )

    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    objects = ClientManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _("Mastodon Client")
        verbose_name_plural = _("Mastodon Clients")
        indexes = [
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return self.client_url

    @property
    def is_authenticated(self):
        """Check if client has completed OAuth flow."""
        return bool(self.access_token and self.client_key and self.client_secret)

    @property
    def has_valid_credentials(self):
        """Check if all required credentials are present."""
        return all([self.client_key, self.client_secret, self.client_url])

    def clean(self):
        """Validate and normalize client_url."""
        from django.core.exceptions import ValidationError
        if self.client_url:
            # Normalize URL (remove trailing slash)
            self.client_url = self.client_url.rstrip('/')
            # Ensure https
            if not self.client_url.startswith(('http://', 'https://')):
                self.client_url = f'https://{self.client_url}'

    def mark_verified(self):
        """Update last_verified timestamp."""
        from django.utils import timezone
        self.last_verified = timezone.now()
        self.save(update_fields=['last_verified'])


class DomainManager(models.Manager):
    """Custom manager for Domain model."""

    def active(self):
        """Return only active domains."""
        return self.filter(is_active=True)

    def bulk_create_or_ignore(self, domain_names):
        """Bulk create domains, ignoring duplicates."""
        domains = [
            Domain(name=name.strip().lower())
            for name in domain_names
            if name.strip()
        ]
        return self.bulk_create(domains, ignore_conflicts=True)


class Domain(models.Model):
    """
    Represents a disposable email domain to be blocked.

    Synced from https://github.com/disposable-email-domains/disposable-email-domains
    """

    # Domain name validator (simplified RFC 1035)
    domain_validator = RegexValidator(
        regex=r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$',
        message=_("Enter a valid domain name"),
        code='invalid_domain'
    )

    name = models.CharField(
        _("Domain Name"),
        max_length=253,
        unique=True,
        validators=[domain_validator],
        db_index=True,
        help_text=_("Disposable email domain to block")
    )

    source = models.CharField(
        _("Source"),
        max_length=50,
        default='disposable-email-domains',
        help_text=_("Source of this domain entry")
    )

    is_active = models.BooleanField(
        _("Active"),
        default=True,
        db_index=True,
        help_text=_("Whether this domain should be blocked")
    )

    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    objects = DomainManager()

    class Meta:
        ordering = ('name',)
        verbose_name = _("Blocked Domain")
        verbose_name_plural = _("Blocked Domains")
        indexes = [
            models.Index(fields=['is_active', 'name']),
        ]

    def __str__(self):
        return self.name

    def clean(self):
        """Normalize domain name."""
        if self.name:
            self.name = self.name.lower().strip()


class Faq(models.Model):
    """
    Frequently Asked Question for the application.
    """

    title = models.CharField(
        _("Title"),
        max_length=200,
        unique=True,
        help_text=_("Question or FAQ title")
    )

    text = models.TextField(
        _("Answer"),
        help_text=_("Answer content (supports HTML)")
    )

    published = models.BooleanField(
        _("Published"),
        default=True,
        db_index=True,
        help_text=_("Whether this FAQ is visible to users")
    )

    order = models.PositiveIntegerField(
        _("Display Order"),
        default=0,
        help_text=_("Sort order (lower numbers appear first)")
    )

    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)

    class Meta:
        ordering = ('order', 'title')
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        indexes = [
            models.Index(fields=['published', 'order']),
        ]

    def __str__(self):
        return self.title