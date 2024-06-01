import re
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from myshop.models import Product, Category, Images, Review, AdditionalInformation
from .forms import ContactForm, SubscriberForm
from .recommender import Recommender
from .tasks import send_form


class HomeView(TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hot_deals'] = Product.objects.exclude(discount__isnull=True).order_by('-created')[:10]
        context['featured_products'] = Product.objects.filter(featured=True)
        context['categories'] = Category.objects.all()
        context['last_five_reviews'] = Review.objects.all().order_by('created_at')[:4]
        return context


class ProductListView(ListView):
    template_name = 'shop/list.html'
    context_object_name = 'productfound'
    paginate_by = 12  # Default number of items per page

    def get_queryset(self):
        count = self.request.GET.get('count')
        if count:
            self.paginate_by = int(count)
            print(f'count is {count}')
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
        context['infos_supplementaires'] = AdditionalInformation.objects.filter(product_id=product.id)
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


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        print(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            print(message)
            send_form.delay(sender, message, request.user.username)
            return redirect(reverse('myshop:home'))
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form})


def politique(request):
    return render(request, 'shop/politique_retours_remb.html')


def quick_view(request,product_id):
    product_quick_view = Product.objects.get(id=product_id)
    images = Images.objects.filter(product_id=product_quick_view.id)
    return render(request, 'shop/product-quick-view.html', {'product_quick_view' : product_quick_view, 'images':images})


@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return JsonResponse({'status': 'success', 'message': 'Votre inscription à la newsletter a bien été prise en compte!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid email address.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
