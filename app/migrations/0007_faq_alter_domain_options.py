# Generated by Django 4.2.10 on 2024-02-18 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_client_client_secret_alter_client_client_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('text', models.TextField()),
                ('published', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.AlterModelOptions(
            name='domain',
            options={'ordering': ('name',)},
        ),
    ]
