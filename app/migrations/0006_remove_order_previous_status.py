# Generated by Django 5.0.1 on 2024-01-11 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_order_previous_status_orderhistory_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='previous_status',
        ),
    ]
