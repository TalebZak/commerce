from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<slug:product_slug>", views.product, name="product"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.add_listing, name="addlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<slug:product_slug>", views.add_watchlist, name="add_watchlist"),
    path("listing/<slug:product_slug>/bid", views.make_bid, name="make_bid"),
    path("listing/<slug:product_slug>/close", views.close_listing, name="close_listing"),
    path("watchlist/delete/<slug:product_slug>",
         views.remove_from_watchlist, name="remove_from_watchlist"),
    path("<str:category>/result", views.category_product, name="category_products"),
    path("category", views.select_category, name="category_select")
]
