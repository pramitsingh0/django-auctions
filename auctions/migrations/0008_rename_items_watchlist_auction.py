# Generated by Django 3.2.8 on 2021-11-09 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='items',
            new_name='auction',
        ),
    ]