# Generated by Django 5.1.1 on 2024-10-12 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0007_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
