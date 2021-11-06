from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    MOTORS = "MOT"
    FASHINON = "FAS"
    ELECTRONICS = "ELE"
    COLLECTIBLES_ARTS = "ART"
    HOME_GARDES = "HGA"
    SPORTING_GOODS = "SPO"
    TOYS = "TOY"
    BUSSINES_INDUSTRIAL = "BUS"
    MUSIC = "MUS"

    CATEGORY = [
        (MOTORS, "Motors"),
        (FASHINON, "Fashion"),
        (ELECTRONICS, "Electronics"),
        (COLLECTIBLES_ARTS, "Collectibles & Art"),
        (HOME_GARDES, "Home & Garden"),
        (SPORTING_GOODS, "Sporting Goods"),
        (TOYS, "Toys"),
        (BUSSINES_INDUSTRIAL, "Business & Industrial"),
        (MUSIC, "Music"),
    ]
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    current_price = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)

    seller = models.CharField(max_length=64)
    imglink = models.URLField(max_length=200, default=None)
    category = models.CharField(max_length=3, choices=CATEGORY)
    open = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id}: {self.title} {self.description}"
class Bids(models.Model):
    pass

class Comments(models.Model):
    pass