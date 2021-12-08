from os import name
from django.urls import path

from . import views
from .forms import (PaymentForm)


app_name = "store"

urlpatterns = [
    path('', views.all_products, name="all_products"),
    path('#', views.all_products, name="modal"),
    path('item/<slug:slug>/', views.product_detail, name="product_detail"),
    path('search/<slug:category_slug>/',
         views.category_list, name='category_list'),
    path('about_us/', views.about_us, name="about-us"),
    path('contact_us/', views.contact_us, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('services/', views.services, name='services'),
    path('update_item/', views.updateItem, name='update_item'),
    path('cart/', views.cart, name='cart'),
    path('initiate_payment/', views.initiate_payment,
         name='initiate-payment'),
    path('delivery/', views.delivery, name='delivery'),



]
