from django.urls import path

from . import views
from . import util
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry_access, name="entry"),
    path("search", views.search, name="search")
]
