from django.db import models
from django.db.models import Avg
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField

from account.models import Customer


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(null=True, blank=True)

    class MPTTMETA:
        order_insertion = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('myshop:product_list_by_category',
                       args=[self.id, self.slug])


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = TreeForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='produits')
    discount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    information = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)  # New field for featured products

    class Meta:
        ordering = ('name',)

    def price_after_Discount(self):
        price = self.price - (self.discount / 100 * self.price)
        return round(price, 2)

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.rating_set.aggregate(Avg('rating'))['rating__avg'] or 0

    @staticmethod
    def get_top_rated_products(limit=5):
        return Product.objects.annotate(avg_rating=Avg('rating__rating')).order_by('-avg_rating')[:limit]

    @staticmethod
    def get_featured_products():
        return Product.objects.filter(featured=True)


class Review(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    review = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.review}"


class Images(models.Model):
    image = models.ImageField(upload_to='produits/subpictures')
    name = models.CharField(max_length=70)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
