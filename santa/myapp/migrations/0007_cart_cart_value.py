# Generated by Django 5.0.6 on 2024-12-23 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_gifts_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_value',
            field=models.IntegerField(default=1),
        ),
    ]
