from _decimal import Decimal
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
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
    return redirect(request.path)


def cart_update(request):
    if request.method == 'POST':
        cart = Cart(request)
        # Extract product_id and quantity from FormData
        for key, value in request.POST.items():
            print(key, value)
            if key.startswith('product_'):
                product_id = int(key.replace('product_', ''))
                quantity = int(value)
                product = get_object_or_404(Product, id=product_id)
                cart.add(product=product, quantity=quantity, override_quantity=True)
        return redirect('cart:cart_detail')
    else:
        # If the request method is not POST or it's not an AJAX request,
        # return a bad request response.
        return HttpResponseBadRequest("Invalid request")


def cart_update_shipping_cost(request):
    if request.method == 'POST':
        shipping_option = request.POST.get('shipping_option')
        shipping_cost = Decimal(shipping_option)  # Convert to Decimal

        # Save shipping cost to session
        request.session['shipping_cost'] = str(shipping_cost)  # Convert Decimal to string

        # Retrieve total price from Cart object
        cart = Cart(request)
        total_with_shipping = cart.get_total_price()

        # Return JSON response with updated shipping cost and total price
        return JsonResponse({'shipping_cost': str(shipping_cost), 'total_with_shipping': str(total_with_shipping)})
    else:
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
