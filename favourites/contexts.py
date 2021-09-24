from django.shortcuts import get_object_or_404
from .models import UsersFavourites


def favourites_products(request):
    favourites_products = []
    if request.user.is_authenticated:
        favourites = get_object_or_404(UsersFavourites, user=request.user)
        favourites_products = favourites.products.all()

    context = {
        "favourites_products": favourites_products,
    }

    return context