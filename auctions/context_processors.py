from .models import AuctionListing

def category_list(request):
    category_list = AuctionListing.CATEGORY
    full_category = [item[1] for item in category_list]
    return {"categories": full_category}