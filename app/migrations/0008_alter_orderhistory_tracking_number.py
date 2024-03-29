# Generated by Django 5.0.1 on 2024-01-11 12:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_orderhistory_tracking_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='tracking_number',
            field=models.CharField(default=django.utils.timezone.now, editable=False, max_length=15, unique=True),
            preserve_default=False,
        ),
    ]
