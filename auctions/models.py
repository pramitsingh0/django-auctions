from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


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
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="bids", null=True)
    bid_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "bid"

    def __str__(self):
        return f"{self.user} bid {self.bid_amount} $ on {self.item.title}"

class Comments(models.Model):
    auction_item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    comments = models.TextField(blank=False, default="Good")
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "comment"
    
    def __str__(self):
        return f"Comment {self.id} on item: {self.auction_item.title} by {self.user.username}"

class Watchlist(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    class Meta:
        verbose_name = "watchlist"
        unique_together = ['auction', 'user']
    def __str__(self):
        return f"{self.auction.title} is on {self.user}'s watchlist"
    