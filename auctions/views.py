from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import widgets, ModelForm
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import AuctionListing, Comments, User, Watchlist, Bids


#-----------------------------------------------#
#--------------------FORMS----------------------#
#-----------------------------------------------#
class CreateListingForms(forms.Form):
    
    """Create Form for Auction Listing Model"""
    title = forms.CharField(label="Item Title", max_length=20, widget=forms.TextInput(attrs={
                                                                    "autocomplete":"off",
                                                                    "label":"title",
                                                                    "class":"form-control"
                                                                }))
    description = forms.CharField(label="Item Description", widget=forms.Textarea(attrs={
                                                                "label":"description",
                                                                "class":"form-control"
                                                            }))
    starting_bid = forms.DecimalField(label="Starting Bid")
    img_link = forms.URLField(label="Image link", widget=forms.URLInput(attrs={
                                                        "class":"form-control"
                                                    }))
    category = forms.ChoiceField(choices=AuctionListing.CATEGORY)
    


    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'seller', 'imglink', 'reporter']

class BiddingForms(forms.Form):
    bid_amount = forms.DecimalField(label="Bid Amount")




# --------------------------------------------------------------#
# -----------------------------VIEWS----------------------------#
# --------------------------------------------------------------#


def index(request):
    active_listing = AuctionListing.objects.filter(open=True)
    return render(request, "auctions/index.html", {
        "auction_items": active_listing
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# --------------------------------------------- #
# ------------------My Views------------------- #
# --------------------------------------------- #
def create_listing_form(request):
    return render(request, "auctions/createListing.html", {
        "forms": CreateListingForms()
    })

@login_required(login_url="login")
def save_listing(request):
    if request.method == "POST":
        form = CreateListingForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            img_link = form.cleaned_data['img_link']
            category = form.cleaned_data['category']
            

        auction_listing = AuctionListing(
            seller = User.objects.get(pk=request.user.id),
            title = title,
            description = description,
            starting_bid = starting_bid,
            category = category,
            imglink = img_link
        )            
        auction_listing.save()
        return redirect('index')

    else:
        return render(request, "auctions/createListing.html", {
            "form": CreateListingForms()
        })

def view_listing(request, auction_id):
    try:
        item = AuctionListing.objects.get(pk=auction_id)
    except:
        return render(request, "auctions/error404.html", {
            "code": 404,
            "message": "Auction Item not found"
        })
    highest_bid = Bids.objects.filter(item=item).order_by('-bid_amount').first()
    if item.open == False:
        if highest_bid is not None:
            winner = highest_bid.user

            # Diffrent view for winner, seller and other users
            if request.user == item.seller:
                return render(request, "auctions/sold.html", {
                    "highest_bid": highest_bid
                })
            elif request.user.id == winner.id:
                return render(request, "auctions/bought.html", {
                    "auction": item
                })
    if request.user.is_authenticated:
        auction_item = Watchlist.objects.filter(auction=auction_id, user=User.objects.get(id=request.user.id)).first()

        if auction_item is not None:
            on_watchlist = True
        else: 
            on_watchlist = False
            
    else:
        on_watchlist = False\

    #fetch comments
    comments = Comments.objects.filter(auction_item=auction_id).order_by('-comment_date')
        
    
    return render(request, "auctions/listingpage.html", {
        "item": item,
        "on_watchlist": on_watchlist,
        "bidding_form": BiddingForms(),
        "highest_bid": highest_bid,
        "comments": comments
    })

@login_required(login_url='login')
def watchlist(request):
    if request.method == "POST":
        watchlist_item = request.POST.get("item_id")
        try:
            item = AuctionListing.objects.get(pk=watchlist_item)
            user = User.objects.get(id=request.user.id)
        except:
            return render(request, "auctions/error404.html", {
                "code": 404,
                "message": "Item doesn't exist"
            })
        
        if request.POST.get("on_watchlist") == "True":
            try:
                remove_watchlist = Watchlist.objects.filter(auction=item, user=user)
                remove_watchlist.delete()
            except:
                return render(request, "auctions/error404.html", {
                    "code": 409,
                    "message": "Error Accessing Watchlist"
                })
            
        else:
            try: 
                add_watchlist = Watchlist(auction=item, user=user)
                add_watchlist.save()
            except:
                return render(request, "auctions/error404.html", {
                    "code": 300,
                    "message": "Cannot save to database"
                })
            
            
        return HttpResponseRedirect("/listingpage/" + watchlist_item)
    else:
        return render(request, "auctions/error404.html")

@login_required(login_url='login')   
def bidding(request):
    if request.method == "POST":
        bid_amount = BiddingForms(request.POST)
        if bid_amount.is_valid():
            bid_amount = float(bid_amount.cleaned_data['bid_amount'])
            auction_id = request.POST.get("item_id")
            try:
                auction = AuctionListing.objects.get(pk=auction_id)
                user = User.objects.get(id=request.user.id)
            except:
                return render(request, "auctions/error404.html", {
                    "code": 309,
                    "message": "Item not found."
                })
            if bid_amount <= 0 or bid_amount < auction.starting_bid:
                return render(request, "auctions/error404.html", {
                    "code": 400,
                    "message": "Bid amount too low."
                })
            
            if auction.seller == user:
                return render(request, "auctions/error404.html", {
                    "code": 400,
                    "message": "Seller cannot bid on his item"
                })
            
            highest_bid = Bids.objects.filter(item=auction).order_by('-bid_amount').first()

            if highest_bid is None or bid_amount > highest_bid.bid_amount:
                
                newbid = Bids(item=auction, user=user, bid_amount=bid_amount)
                newbid.save()

                auction.current_price = bid_amount
                auction.save()

                return HttpResponseRedirect("/listingpage/" + auction_id)
                
            else:
                return render(request, "auctions/error404.html", {
                    "code": 300,
                    "message": "Cannot place bid. Bid value lower then highest bid"
                })
        else:
            return render(request, "auctions/error404.html", {
                    "code": 300,
                    "message": "Invalid Bid"
                })

@login_required(login_url='login')
def close_auction(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        auction_item = AuctionListing.objects.get(pk=item_id)
        auction_item.open = False
        auction_item.save()
        highest_bid = Bids.objects.filter(item=auction_item).order_by('-bid_amount').first()
        return render(request, "auctions/sold.html", {
            "highest_bid": highest_bid
        })
    return redirect('index')

def add_comments(request):
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        comment = request.POST.get("comment")
        auction_item = AuctionListing.objects.get(pk=item_id)
        user = User.objects.get(id=request.user.id)
        new_comment = Comments(auction_item=auction_item, user=user, comments=comment)
        new_comment.save()
        return HttpResponseRedirect("/listingpage/" + item_id)
        
    else:
        return render(request, "error404.html", {
            "code": 404,
            "message": "Method not allowed"
        })

@login_required(login_url='login')
def view_watchlist(request):
    watchlist_auctions_ids = User.objects.get(id=request.user.id).watchlist.values_list("auction")
    watchlist_items = AuctionListing.objects.filter(id__in=watchlist_auctions_ids)
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

def categories(request):
    category_list = AuctionListing.CATEGORY
    full_category = [item[1] for item in category_list]

    
    return render(request, "auctions/categories.html", {
        "categories": full_category,

    })

def view_categories(request, type):
    category_list = AuctionListing.CATEGORY
    full_category = [x[1] for x in category_list]
    if type in full_category:
        short_category = [x[0] for x in category_list if type == x[1]]
        category_item = AuctionListing.objects.filter(category=short_category[0])
        return render(request, "auctions/view_category.html", {
            "category_items": category_item,
            "head": type
        })