from django.core.paginator import Paginator
from django.shortcuts import (render, get_object_or_404,
                              redirect, reverse, HttpResponse)
from django.contrib import messages
from django.http import HttpResponseRedirect


from .models import UsersFavourites
from products.models import Product


def view_favourites(request):
    ''' a view to show the users favourites '''

    favourite_products = []

    favourites = UsersFavourites.objects.get(user=request.user)

    for product in favourites.products.all():
        favourite_products.append(product)

    template = "favourites/favourites.html"

    context = {
        "favourites": True,
        "favourite_products": favourite_products,
    }

    return render(request,
                  template,
                  context)


def add_to_favourites(request, product_id):

    redirect_url = request.POST.get("redirect_url")

    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        print(f"adding product {product}")
        favourites = get_object_or_404(UsersFavourites, user=request.user)
        if product not in favourites.products.all():
            favourites.products.add(product)
            messages.success(request,
                             f"{product.name} has been added to your \
                                 favourites.")
            return redirect(redirect_url)
    else:
        messages.error(request,
                       "You do not have permission to do this.")
        return redirect(redirect_url)


def remove_from_favourites(request, product_id):
    ''' View to remove products from the favourites '''

    redirect_url = request.POST.get("redirect_url")

    if request.method == "POST":
        try:
            product = get_object_or_404(Product, pk=product_id)
            favourites = get_object_or_404(UsersFavourites, user=request.user)
            print(product)
            print(favourites)
            if product in favourites.products.all():
                favourites.products.remove(product)
            messages.success(request,
                                f"{product.name} has been removed \
    from your favourites.")
            return redirect(redirect_url)
        except Exception as error:
            messages.error(request, f"Error removing product {error}")
            return HttpResponse(status=500)
    else:
        messages.error(request, "Error you do not have \
permission to do this.")
        return redirect(redirect_url)


def empty_favourites(request):
    ''' A view to empty the favourites '''

    redirect_url = request.POST.get("redirect_url")

    if request.method == "POST":
        favourites = get_object_or_404(UsersFavourites, user=request.user)
        favourites.products.clear()
        messages.success(request, "Your favourites list has been emptied.")
        return redirect(redirect_url)
    else:
        messages.error(request, "Error you do not have \
permission to do this.")
        return redirect(redirect_url)
