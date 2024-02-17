import csv

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import reverse
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Product, Images, Rating


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count',)
    list_display_links = ('indented_title',)

    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'created', 'updated', 'featured', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Images)
class ImagesAdmin(ModelAdmin):
    list_display = ['name']
    list_display_links = ('name',)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('product', 'created_at')
    search_fields = ('user__username', 'product__name')
    date_hierarchy = 'created_at'


admin.site.register(Rating, RatingAdmin)
