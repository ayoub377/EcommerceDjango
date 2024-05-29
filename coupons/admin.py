from django.contrib import admin

from coupons.models import Coupon


# Register your models here.

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = ['code', 'valid_from', 'valid_to',
                    'discount', 'active', 'is_used']
    list_filter = ['active', 'valid_from', 'valid_to', 'is_used']
    search_fields = ['code']
