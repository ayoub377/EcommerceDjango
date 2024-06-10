from _decimal import Decimal
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from coupons.forms import CouponApplyForm
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


def cart_update(request):
    if request.method == 'POST':
        cart = Cart(request)
        # Extract product_id and quantity from FormData
        for key, value in request.POST.items():
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


@csrf_exempt
def cart_update_shipping_cost(request):
    if request.method == 'POST':
        shipping_option = request.POST.get('shipping_option')
        try:
            shipping_cost = Decimal(shipping_option)
        except InvalidOperation:
            return HttpResponseBadRequest("Invalid shipping cost")

        request.session['shipping_cost'] = str(shipping_cost)

        cart = Cart(request)
        total_with_shipping = cart.get_total_price_after_discount()

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

    r = Recommender()

    cart_products = [item['product'] for item in cart]

    coupon_apply_form = CouponApplyForm()

    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []

    print(f'recommended products are : {recommended_products}')
    return render(request, 'cart/detail.html', {'cart': cart,'recommended_products':recommended_products,'coupon_apply_form': coupon_apply_form})
