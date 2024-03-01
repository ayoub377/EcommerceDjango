import re
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from myshop.models import Product, Category, Images
from .recommender import Recommender


class HomeView(TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_deals'] = Product.objects.exclude(discount__isnull=True).order_by('-created')[:10]
        context['featured_products'] = Product.objects.filter(featured=True)
        context['categories'] = Category.objects.all()
        return context


class ProductListView(ListView):
    template_name = 'shop/list.html'
    context_object_name = 'productfound'
    paginate_by = 12  # Default number of items per page

    def get_queryset(self):
        count = self.request.GET.get('count')
        if count:
            self.paginate_by = int(count)
        categor_slug = self.kwargs['categor_slug']
        my_category = get_object_or_404(Category, slug=categor_slug)
        return Product.objects.filter(category__in=my_category.get_descendants(include_self=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categor_slug = self.kwargs['categor_slug']
        my_category = get_object_or_404(Category, slug=categor_slug)
        context['category'] = my_category
        # Fetch featured products
        context['featured_products'] = Product.objects.filter(featured=True)
        return context


def product_search_view(request):
    query = request.GET.get('query')
    cat_id = request.GET.get('cat')

    # Convert query to lowercase for case insensitivity
    query_lower = query.lower() if query else None

    # Extract keywords from the query
    keywords = [keyword.lower() for keyword in re.findall(r'\b\w{3,}\b', query)] if query else []

    # Use Q objects to build a complex query for partial matches
    search_filter = Q()
    for keyword in keywords:
        search_filter |= Q(name__icontains=keyword) | Q(description__icontains=keyword)

    # Apply category filter if provided
    if cat_id:
        search_filter &= Q(category_id=cat_id)

    # Execute the filtered query
    queryset = Product.objects.filter(search_filter).order_by('-price')

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'results': page_obj,
    }

    return render(request, 'shop/search.html', context)


class ProductDetailView(TemplateView):
    template_name = 'shop/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        context['product'] = product
        context['images'] = Images.objects.filter(product_id=product.id)
        context['featured_products'] = Product.objects.filter(featured=True)[:3]
        context['latest_products'] = Product.objects.order_by('-created')[:3]
        r = Recommender()
        context['recommended_products'] = r.suggest_products_for([product], 4)
        return context


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=q)
        results = [product.name for product in products]
        return JsonResponse(results, safe=False)
    return JsonResponse({'error': 'Fail'})
