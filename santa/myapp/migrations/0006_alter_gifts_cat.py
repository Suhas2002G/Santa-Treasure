# Generated by Django 5.0.6 on 2024-12-19 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_address_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifts',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Statue'), (2, 'Tree'), (3, 'Decorations'), (4, 'Cloths')], verbose_name='category'),
        ),
    ]
