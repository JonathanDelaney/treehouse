from django import template
from products.models import Product
from django.shortcuts import get_object_or_404


register = template.Library()


@register.filter(name='ifinlist')
def ifinlist(value, list):
    product = get_object_or_404(Product, pk=value)
    if product in list:
        return True