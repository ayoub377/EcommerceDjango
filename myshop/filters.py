import django_filters

from myshop.forms import RangeForm
from myshop.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['price']
        form = RangeForm
