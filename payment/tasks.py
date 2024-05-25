# from celery import app
#
# from orders.models import Order
# from django.core.mail import EmailMessage
# from easy_pdf.rendering import render_to_pdf
#
#
# def payment_completed(order_id):
#     order = Order.objects.get(id=order_id)
#     subject = f'My Shop - EE Invoice no. {order.id}'
#     message = 'sil vous plait,veuillez recuperer votre recu.'
#     email = EmailMessage(subject, message, 'tommypep20@gmail.com', [order.email])
#     pdf = render_to_pdf('orders/order/pdf.html', {'order': order})
#     email.attach(f'order_{order.id}.pdf', pdf, 'application/pdf')
#     email.send()
