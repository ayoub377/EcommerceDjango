from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Customer

# Register your models here.

admin.site.register(Customer)
