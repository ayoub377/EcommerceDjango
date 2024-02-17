from django.db import models

from account.models import Customer
from myshop.models import Product

type_paiements = [
    ('paiement par carte bancaire', 'paiement par carte bancaire'),
    ('paiement sur livraison', 'paiement sur livraison')
]


class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    prenom = models.CharField('prenom', max_length=50)
    nom = models.CharField('nom', max_length=50)
    email = models.EmailField()
    addresse = models.CharField('adresse', max_length=250)
    telephone = models.CharField('telephone', max_length=12)
    code_postal = models.CharField('code postal', max_length=20)
    ville = models.CharField('ville', max_length=100)
    type_paiement = models.CharField(max_length=30, choices=type_paiements, default=type_paiements[0][0])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
