# Generated by Django 5.0.1 on 2024-01-10 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(editable=False, max_length=15, unique=True),
        ),
    ]