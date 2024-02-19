from django.db import models


class Client(models.Model):
    """

    Model class representing a client.

    Attributes:
    - client_id (str): The client's ID.
    - client_secret (str): The client's secret.
    - client_url (str): The client's URL.
    - access_token (str, optional): The client's access token.
    - created_at (datetime): The timestamp when the client was created.

    Methods:
    - __str__(): Returns the client's URL as a string.

    """
    client_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
    client_secret = models.CharField(max_length=255,  null=False, blank=False)
    client_url = models.CharField(max_length=255, null=False, blank=False)
    access_token = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.client_url


class Domain(models.Model):
    """
    Class: Domain

    Represents a domain in the system.

    Attributes:
    - name: A CharField that holds the name of the domain. It has a maximum length of 100 characters and is unique, not nullable, and not blank.
    - created_at: A DateTimeField that holds the date and time when the domain was created. It is automatically set to the current date and time when the domain is created.

    Methods:
    - __str__(): Returns the name of the domain as a string.

    """
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Faq(models.Model):
    """
    Faq Model

    This class represents a frequently asked question (FAQ) in the application. It defines the fields and behaviors of an FAQ.

    Attributes:
        title (CharField): The title of the FAQ, limited to 100 characters.
        text (TextField): The content of the FAQ.
        published (BooleanField): Indicates whether the FAQ is published or not. Default is True.
        created_at (DateTimeField): The date and time when the FAQ was created.

    Meta:
        ordering (tuple): Specifies the default ordering of FAQs by title in ascending order.

    Methods:
        __str__(): Returns a string representation of the FAQ.

    """
    title = models.CharField(max_length=100, unique=True, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    published = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title
