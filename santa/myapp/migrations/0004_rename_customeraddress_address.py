# Generated by Django 5.0.6 on 2024-12-17 14:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_customeraddress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerAddress',
            new_name='Address',
        ),
    ]
