# Generated by Django 5.0.3 on 2024-04-01 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_wishlist_rename_created_product_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['province', 'district', 'city', 'street', 'customer']},
        ),
        migrations.AlterModelOptions(
            name='auction',
            options={'ordering': ['product', 'current_price', 'ending_time', 'auction_status', 'created_at', 'updated_at']},
        ),
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['bidder', 'amount', 'status', 'created_at']},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['membership']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['product']},
        ),
        migrations.AlterModelOptions(
            name='usercoin',
            options={'ordering': ['user', 'balance', 'created_at', 'updated_at']},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='starting_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='number_of_bids',
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
