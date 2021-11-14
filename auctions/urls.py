from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting/", views.create_listing_form, name="createListing"),
    path("savelisting/", views.save_listing, name="save"),
    path("listingpage/<int:auction_id>", views.view_listing, name="listingPage"),
    path("watchlistadd/", views.watchlist, name="watchlist" ),
    path("bid", views.bidding, name="bid"),
    path("close", views.close_auction, name="close"),
    path("addcomment", views.add_comments, name="addcomment")
]