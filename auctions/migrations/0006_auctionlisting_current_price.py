# Generated by Django 3.2.8 on 2021-11-06 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_auctionlisting_current_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=11),
        ),
    ]