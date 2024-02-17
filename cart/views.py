from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from myshop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from myshop.recommender import Recommender


def cart_Add_list(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product,
             quantity=1)
    return redirect('cart:cart_detail')


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
