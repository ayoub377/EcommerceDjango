from django.shortcuts import get_object_or_404
from .models import Category, Product


def list_categories(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
    return {'categories': categories, 'category': category}


def hot_prods(request):
    products = Product.objects.all().order_by('created')[:3]
    return {'products': products}



