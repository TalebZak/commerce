from django import template
from ..models import Watchlist, Product

register = template.Library()


@register.filter(name='search')
def is_in(value, product_id):
    for element in value:
        if product_id == element.id:
            return True
    return False
