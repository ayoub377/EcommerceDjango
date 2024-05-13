from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from myshop.recommender import Recommender
from orders.tasks import order_created
from account.models import Customer
from .models import OrderItem
from .forms import OrderCreateForm

from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa



@login_required
def Order_create(request):
    cart = Cart(request)
    products_list = []
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            username = request.user.username
            customer, _ = Customer.objects.get_or_create(username=username)
            order.customer = customer
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
                products_list.append(item['product'])

            r = Recommender()
            r.products_bought(products_list)

            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            # Redirect for payment based on the selected payment type
            return redirect(reverse('orders:Order_created'))

    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


def order_created_view(request):
    return render(request, 'orders/order/created.html')


@staff_member_required
def render_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    pisa.CreatePDF(html, dest=response)
    return response
