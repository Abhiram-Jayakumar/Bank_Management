# Generated by Django 5.1.1 on 2024-10-12 06:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0004_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('account_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('Adhaar', models.CharField(max_length=16, unique=True)),
                ('Pan', models.CharField(max_length=15, unique=True)),
                ('vstatus', models.IntegerField(default=0)),
            ],
        ),
    ]
