# Generated by Django 5.0.6 on 2024-12-12 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gifts',
            old_name='gdetails',
            new_name='pdetails',
        ),
        migrations.AlterField(
            model_name='gifts',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Statue'), (2, 'Tree'), (3, 'Cap'), (4, 'Cloths')], verbose_name='category'),
        ),
    ]