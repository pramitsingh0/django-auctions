from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    seller = models.CharField(max_length=64)
    imglink = models.CharField(max_length=200, default=None)
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.title}"
class Bids(models.Model):
    pass

class Comments(models.Model):
    pass