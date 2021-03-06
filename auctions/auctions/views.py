from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import *
from .models import *

"""the page that the user would say when they get to the site,
   returns all the products along with a category form to allow filtering"""
def index(request):
    return render(request, "auctions/index.html", {
        "products": Product.objects.all(),
        "categoryform": CategorySelectionForm
    })

"""a close listing method, to allow the owner of the product to close the bidding"""
def close_listing(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    product.status = False
    product.save(update_fields=['status'])
    return HttpResponseRedirect(reverse('product', args=(product_slug,)))

"""to allow a user to remove a product from his watchlist"""
def remove_from_watchlist(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    watchlist_item = Watchlist.objects.get(product=product)
    watchlist_item.delete()
    return HttpResponseRedirect(reverse('watchlist'))


def add_listing(request):
    if request.method == "POST":
        form = ListingCreationForm(request.POST, request.FILES)
        if form.is_valid():
            newlisting = form.save(commit=False)# saves the content of the form in a class instance without inserting it in the DB
            newlisting.owner = request.user
            newlisting.save()#save the product in the DB
            return HttpResponseRedirect(reverse('product', args=(newlisting.get_url_path(),)))
        return render(request, "auctions/listingcreation.html", {
            "addform": form
        })
    return render(request, "auctions/listingcreation.html", {
        "addform": ListingCreationForm()
    })

"""filtering the products by category"""
def category_product(request, category):
    category_products = Product.objects.filter(product_type=category)
    return render(request, "auctions/category_products.html", {
        "products": category_products
    })


def select_category(request):
    if request.method == "POST":
        categoryform = CategorySelectionForm(request.POST)
        if categoryform.is_valid():
            category = categoryform.cleaned_data["product_type"]
            return HttpResponseRedirect(reverse('category_products', args=(category,)))

        return HttpResponseRedirect(reverse('index'))
    return HttpResponseRedirect(reverse('index'))

"""the content of a user's watchlist is returned to be displayed on the watchlist page"""
@login_required# a user who isn't signed in doesn't have a watchlist
def watchlist(request):
    my_watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "products": [element.product for element in my_watchlist]# returning all products in the user's watchlist
    })


@login_required
def add_watchlist(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    user = request.user
    new_watchlist_element = Watchlist.objects.create(user=user, product=product)
    return HttpResponseRedirect(reverse('watchlist'))


@login_required
def make_bid(request, product_slug):
    theproduct = get_object_or_404(Product, slug=product_slug)
    product_bids = theproduct.bids.all()
    comments = theproduct.comments.all()
    if request.method == "POST":
        bidding_form = BiddingForm(request.POST)
        if bidding_form.is_valid():
            bidding_form.full_clean()
            newbid = bidding_form.save(commit=False)
            if newbid.value <= theproduct.price or newbid <= product_bids.order_by('-value').first():
                """if a bid's value is less than the product's price or less than a product's highest bid, the bidding is cancelled"""
                return render(request, "auctions/product.html", {
                    "watchlist": Watchlist.objects.filter(user=request.user),
                    "bids": product_bids,
                    "biddingform": BiddingForm(),
                    "commentform": CommentForm(),
                    "comments": comments,
                    "product": theproduct
                })
            """if the bidding is successful it gets saved"""
            newbid.bidder = request.user
            newbid.listing = theproduct
            newbid.save()
            return HttpResponseRedirect(reverse('product', args=(product_slug,)))
    return render(request, "auctions/product.html", {
        "watchlist": Watchlist.objects.filter(user=request.user),
        "bids": product_bids,
        "biddingform": BiddingForm(),
        "commentform": CommentForm(),
        "comments": comments,
        "product": theproduct
    })

"""generate a product's page, with bids and comments"""
def product(request, product_slug):
    theproduct = get_object_or_404(Product, slug=product_slug)
    comments = theproduct.comments.all()
    product_bids = theproduct.bids.all()
    """adding comments to a product"""
    if request.method == "POST":
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            commentform.full_clean()
            new_comment = commentform.save(commit=False)
            new_comment.listing = theproduct
            new_comment.writer = request.user
            new_comment.save()
    watchlist = None
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/product.html", {
        "watchlist":  watchlist,
        "currentbid": product_bids.order_by('-value').first(),
        "biddingform": BiddingForm(),
        "commentform": CommentForm(),
        "comments": comments,
        "product": theproduct
    })

"""the login method to allow the user to get connected in the app"""
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


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]
            if password != confirmation:
                return render(request, "auctions/register.html", {
                    "RegistrationForm": RegistrationForm(),
                    "message": "Passwords must match."
                })
            """to avoid the issue of duplicate emails in the app"""
            if User.objects.filter(email=email).exists():
                return render(request, "auctions/register.html", {
                    "RegistrationForm": RegistrationForm(),
                    "message": "Email already exists"
                })
                # Attempt to create new user
            try:
                user = User.objects.create_user(username, email,
                                                password,
                                                first_name=first_name, last_name=last_name)
                user.save()
            except IntegrityError:
                return render(request, "auctions/register.html", {
                    "RegistrationForm": RegistrationForm(),
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            "RegistrationForm": RegistrationForm()
        })
