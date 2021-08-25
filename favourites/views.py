from django.core.paginator import Paginator
from django.shortcuts import (render, get_object_or_404,
                              redirect, reverse, HttpResponse)
from django.contrib import messages

from .models import UsersFavourites
from products.models import Product


def view_favourites(request):
    ''' a view to show the users favourites '''

    favourite_products = []
    favourites = request.session.get("favourites", {})

    for product_id in favourites:
        product = get_object_or_404(Product, pk=product_id)
        favourite_products.append({"product": product})

    template = "favourites/favourites.html"
    print(favourite_products)
    context = {
        "favourites": True,
        "favourite_products": favourite_products,
    }

    return render(request,
                  template,
                  context)


def add_to_favourites(request, product_id):
    # product = get_object_or_404(product, pk=product_id)

    favourites = request.session.get("favourites", {})
    redirect_url = request.POST.get("redirect_url")

    favourites[product_id] = product_id
    request.session["favourites"] = favourites

    return redirect(redirect_url)
