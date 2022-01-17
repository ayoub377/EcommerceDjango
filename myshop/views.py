import json
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from myshop.models import Product, Category, Images
from .filters import ProductFilter
from .recommender import Recommender
from .forms import RangeForm


def home(request):
    hot_deals = Product.objects.exclude(discount__isnull=True).order_by('created')
    return render(request, 'shop/home.html', {'hot_deals': hot_deals})


def list_prods_categories(request, id, categor_slug):
    my_category = Category.objects.filter(slug=categor_slug)
    productfound = Product.objects.filter(category__in=my_category.get_descendants(include_self=True))
    values = [p.price for p in productfound]
    min_val = round(min(values))
    max_val = round(max(values))
    range_form = RangeForm()
    return render(request, 'shop/list.html',
                  {'range_form': range_form, 'min_val': min_val, 'max_val': max_val, 'id': id,
                   'categor_slug': categor_slug, 'productfound': productfound})


def range_filter(request, id, categor_slug):
    my_category = Category.objects.filter(slug=categor_slug)
    productfound = Product.objects.filter(category__in=my_category.get_descendants(include_self=True))
    values = [p.price for p in productfound]
    min_val = round(min(values))
    max_val = round(max(values))
    range_form = RangeForm(request.GET)
    minimum = request.GET.get('min_value')
    maximum = request.GET.get('max_value')
    productista = productfound.filter(price__range=(minimum, maximum))
    return render(request, 'shop/list.html',
                  {'range_form': range_form, 'min_val': min_val, 'max_val': max_val, 'id': id,
                   'categor_slug': categor_slug, 'productista': productista})


def product_search(request):
    query = None
    results = []
    if request.method == 'GET':
        query = request.GET['query']
        search_vector = SearchVector('name', 'description')
        search_query = SearchQuery(query)
        results = Product.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)). \
            filter(search=search_query).order_by('-price')
    return render(request, 'shop/search.html',
                  {
                      'query': query,
                      'results': results})


def details(request, pk):
    product = get_object_or_404(Product, id=pk)
    images = Images.objects.filter(product_id=product.id)
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request, "shop/details.html",
                  {'product': product, 'images': images, 'recommended_products': recommended_products})


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=q)
        results = []
        for rs in products:
            product_json = {}
            product_json = rs.name
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
