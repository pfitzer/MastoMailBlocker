# Generated by Django 4.2.10 on 2024-02-19 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_client_access_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='client_id',
            new_name='client_key',
        ),
    ]
