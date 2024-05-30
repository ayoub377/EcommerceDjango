from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Product
from django.contrib import messages
from .forms import SubscriberForm


def list_categories(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
    return {'categories': categories, 'category': category}


def get_featured_products(request):
    featured_products = Product.objects.filter(featured=True)
    return {
        'featured_products': featured_products
    }

def newsletter_form(request):
    form = SubscriberForm(request.POST)
    return {
        'newsletter_form': form
    }
