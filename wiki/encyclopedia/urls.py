from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry_access, name="entry"),
    path("<str:search_string>", views.search, name="search")
]
