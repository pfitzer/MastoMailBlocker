# Generated by Django 4.2.10 on 2024-02-18 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_domain_remove_client_code_remove_client_scope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='client_secret',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_url',
            field=models.CharField(max_length=255),
        ),
    ]
