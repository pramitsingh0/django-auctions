# Generated by Django 3.2.8 on 2021-11-05 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]