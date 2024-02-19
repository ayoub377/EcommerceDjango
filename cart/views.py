import json

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from myshop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from myshop.recommender import Recommender


def cart_Add_list(request, product_id):
    print('added to the cart')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product,
             quantity=1)
    return redirect('cart:cart_detail')


def cart_update(request):
    if request.method == 'POST':
        cart = Cart(request)
        print(request.POST.items())
        # Extract product_id and quantity from FormData
        for key, value in request.POST.items():
            print(key, value)
            if key.startswith('product_'):
                product_id = int(key.replace('product_', ''))
                quantity = int(value)
                product = get_object_or_404(Product, id=product_id)
                cart.add(product=product, quantity=quantity,override_quantity=True)

        return redirect('cart:cart_detail')
    else:
        # If the request method is not POST or it's not an AJAX request,
        # return a bad request response.
        return HttpResponseBadRequest("Invalid request")


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    previous_url = request.POST.get('next')
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=int(cd['quantity']),
                 override_quantity=cd['override'])

        if previous_url:
            return redirect(previous_url)
        else:
            return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if len(cart) > 0:
        return redirect('cart:cart_detail')
    else:
        return redirect('myshop:home')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    # r = Recommender()
    # cart_products = [item['product'] for item in cart]
    # r.products_bought(cart_products)
    # recommended_products = r.suggest_products_for(cart_products, max_results=4)
    return render(request, 'cart/detail.html', {'cart': cart})
