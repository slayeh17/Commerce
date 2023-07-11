from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_available=True),
        "message": "Active Listings",
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
            
    elif request.method == "GET":
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

    elif request.method == "GET":
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        img_url = request.POST["img_url"]
        bid = request.POST["bid"]
        category = request.POST["category"]
        length = request.POST["length"]
        owner = request.user

        cc = Category.objects.get(category_core=category)
        bid_obj = Bid(
            bid=float(bid),
            user=owner,
        )
        bid_obj.save()

        new_listing = Listing(
            title=title,
            description=description,
            img_url=img_url,
            bid=bid_obj,
            category=cc,
            length=length,
            owner=owner,
        )
        new_listing.save()

        return HttpResponseRedirect(reverse("index"))

    elif request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "Category": Category.objects.all()
        })

def core_list(request):
    if request.method == "POST":
        core = request.POST["core"]
        coreObj = Category.objects.get(category_core=core)
        return render(request, "auctions/core.html", {
            "listings": Listing.objects.filter(category=coreObj, is_available=True),
            "core": core,
            "show_listings": True,
        })
    elif request.method == "GET":
        return render(request, "auctions/core.html", {
            "Category": Category.objects.all(),
            "show_listings": False,
        })

def listing(request, id):
    listing = Listing.objects.get(pk=id)
    comments = Comment.objects.filter(listing=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": request.user in listing.watchlist.all(),
        "comments": comments,
        "is_owner": listing.owner.username == request.user.username,
        "bidder": listing.bid.user,
    })

def add_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    listing.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def remove_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    listing.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def watchlist_listings(request):
    listings = request.user.user_watchlist.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "message": "Wands under Watchlist",
    })

def comment(request, id):
    comment_text = request.POST["comment_text"]
    listing = Listing.objects.get(pk=id)
    com_obj = Comment(
        author=request.user,
        listing=listing,
        comment_text=comment_text,
    )
    com_obj.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def bid(request, id):
    current_bid = int(request.POST["bid_price"])
    listing = Listing.objects.get(pk=id)
    if current_bid > listing.bid.bid:
        bid_obj = Bid(
            user=request.user,
            bid=current_bid,
        )
        bid_obj.save()
        listing.bid = bid_obj
        listing.save()
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": request.user in listing.watchlist.all(),
        "comments": Comment.objects.filter(listing=listing),
        "update": True,
        "bidder": listing.bid.user,
        })
    else:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "in_watchlist": request.user in listing.watchlist.all(),
        "comments": Comment.objects.filter(listing=listing),
        "update": False,
        "bidder": listing.bid.user,
        })

def close_listing(request, id):
    listing = Listing.objects.get(pk=id)
    listing.is_available = False
    listing.save()
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_available=True),
        "message": "Active Listings",
    })

def closed(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_available=False),
        "message": "Closed Listings",
    })