# Generated by Django 5.0.4 on 2024-04-18 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0017_rename_user_delivery_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auction.auction'),
        ),
    ]
