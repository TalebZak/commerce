from django import template
from ..models import Watchlist, Product

register = template.Library()


@register.filter(name='search')
def is_in(value, product_name):
    product = Product.objects.get(name=product_name)
    for element in value:
        if product == element.product:
            return True
    return False
