from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Order, OrderItem


@shared_task
def order_created(order_id):
    order = get_object_or_404(Order, id=order_id)
    subject = f'Order nr. {order.id}'

    # Prepare context for rendering the email template
    context = {
        'order': order,
        'items': OrderItem.objects.filter(order=order),
    }

    if order.type_paiement == 'paiement sur livraison':
         # Render HTML content for delivery
        html_content = render_to_string('orders/order/email/order_confirmation_livraison.html', context)
        text_content = strip_tags(html_content)  # this strips the html, so people will have the text as well.
    else:
         # Render HTML content for delivery
        html_content = render_to_string('orders/order/email/order_confirmation_bank_transfer.html', context)
        text_content = strip_tags(html_content)  # this strips the html, so people will have the text as well.

    # email client setup to send the email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        'contact@jouetspalace.com',
        [order.email]
    )

    email.attach_alternative(html_content, 'text/html')
    email.send()
