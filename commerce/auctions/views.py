from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .Forms import *
from .models import *
import datetime as dt


def index(request):
    return render(request, "auctions/index.html", {
        "products": Product.objects.all()
    })


def add_listing(request):
    if request.method == "POST":
        form = ListingCreationForm()
        if form.is_valid():
            price = form.cleaned_data["price"]
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            owner = request.user
            post_date = form.cleaned_data["date_posted"]
            newlisting = Product(price, name, description, category, owner, post_date)
            newlisting.save()
            return HttpResponseRedirect(reverse('product'), kwargs={'product_name': newlisting.name})
        return render(request, "auctions/listingcreation.html", {
            "addform": form
        })
    return render(request, "auctions/listingcreation.html", {
        "addform": ListingCreationForm()
    })


def product(request, product_name):
    theproduct = Product.objects.get(name=product_name)
    return render(request, "auctions/product.html", {
        "product": theproduct
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
