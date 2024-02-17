from django.contrib.auth.models import User, AbstractUser
from django.db import models


# Create your models here.

class Customer(AbstractUser):
    username = models.CharField(max_length=250, unique=True)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    telephone = models.CharField(max_length=12)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.username
