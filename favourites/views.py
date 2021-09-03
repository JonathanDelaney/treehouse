from django.core.paginator import Paginator
from django.shortcuts import (render, get_object_or_404,
                              redirect, reverse, HttpResponse)
from django.contrib import messages
from django.http import HttpResponseRedirect


from .models import UsersFavourites
from products.models import Product


def view_favourites(request):
    ''' a view to show the users favourites '''

    # template = "favourites/favourites.html"
    # return render(request,
    #               template)
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

    # return redirect(redirect_url)

    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        favourites = get_object_or_404(UsersFavourites, user=request.user)
        if product not in favourites.products.all():
            favourites.products.add(product)
            messages.success(request,
                             f"{product.name} has been added to your favourites.")
            return HttpResponse(status=200)
    else:
        messages.error(request,
                       "You do not have permission to do this.")
        return HttpResponseRedirect(request.path_info)
