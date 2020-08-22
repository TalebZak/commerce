from django.urls import path

from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry_access, name="entry"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("random", views.random_entry, name="random")
]
