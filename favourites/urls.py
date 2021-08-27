from django.urls import path
from . import views


urlpatterns = [
    path("", views.view_favourites, name="view_favourites"),
    path("add/tofavourites/<product_id>",
         views.add_to_favourites,
         name="add_to_favourites"),
]