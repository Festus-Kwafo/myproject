from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.site_header = 'Yotech Systems Admin'
admin.site.unregister(Group)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor', 'slug',
                    'price', 'in_stock', 'created', 'updated', 'is_featured', 'category']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock', 'is_featured']
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'role']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']
    list_filter = ('created',)


admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
admin.site.register(Payment)
