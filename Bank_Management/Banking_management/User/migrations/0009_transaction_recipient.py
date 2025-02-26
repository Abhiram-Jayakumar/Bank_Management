# Generated by Django 5.1.1 on 2024-10-12 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_user_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='recipient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='received_transactions', to='User.user'),
            preserve_default=False,
        ),
    ]
