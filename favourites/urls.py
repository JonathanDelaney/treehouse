from django.urls import path
from . import views


urlpatterns = [
    path("", views.view_favourites, name="view_favourites"),
    path("add/<product_id>/", views.add_to_favourites,
         name="add_to_favourites"),
    path("remove/<product_id>/", views.remove_from_favourites,
         name="remove_from_favourites"),
    path("empty/", views.empty_favourites,
         name="empty_favourites"),
]
