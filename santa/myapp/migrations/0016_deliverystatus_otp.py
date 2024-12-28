# Generated by Django 5.0.6 on 2024-12-26 09:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_alter_order_aid'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('oid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_status', to='myapp.order')),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=4)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('oid', models.ForeignKey(db_column='oid', on_delete=django.db.models.deletion.CASCADE, to='myapp.order')),
            ],
        ),
    ]