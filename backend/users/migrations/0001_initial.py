# Generated by Django 5.1.7 on 2025-03-15 05:46

import django.db.models.deletion
import secrets
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=255)),
                ('store_email', models.EmailField(max_length=254, unique=True)),
                ('store_address', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('verified', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryPartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('verified', models.BooleanField(default=False)),
                ('is_available', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SellerToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=secrets.token_hex, max_length=255, unique=True)),
                ('seller', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.seller')),
            ],
        ),
    ]
