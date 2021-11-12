from django.contrib import admin
from .models import AuctionListing, Bids, Watchlist
# Register your models here.

admin.site.register(AuctionListing)
admin.site.register(Watchlist)
admin.site.register(Bids)