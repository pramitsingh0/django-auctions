# Generated by Django 3.2.8 on 2021-11-05 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211105_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=models.DecimalField(decimal_places=2, max_digits=8, null=True), max_digits=8, null=True),
        ),
    ]
