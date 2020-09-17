from django import template
from django.shortcuts import get_object_or_404

from ..models import Watchlist, Product

register = template.Library()


@register.filter(name='search')
def is_in(value, product_slug):
    try:
        product = Product.objects.get(slug=product_slug)
    except Product.DoesNotExist:
        return False
    for element in value:
        if product == element.product:
            return True
    return False
