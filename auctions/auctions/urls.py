from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<str:product_name>", views.product, name="product"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.add_listing, name="addlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<str:product_name>", views.add_watchlist, name="add_watchlist"),
    path("listing/<str:product_name>/bid", views.make_bid, name="make_bid"),
    path("listing/<str:product_name>/close", views.close_listing, name="close_listing"),
    path("watchlist/delete/<str:product_name>",
         views.remove_from_watchlist, name="remove_from_watchlist"),
    path("<str:category>/result", views.category_product, name="category_products"),
    path("category", views.select_category,name="category_select")
]
