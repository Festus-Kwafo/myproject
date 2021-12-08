from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.db.models.expressions import Case
from django.urls import reverse

from core.settings import AUTH_USER_MODEL

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'catogories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='product', on_delete=CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='image/')
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    product_type = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    product_details = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])


class Customer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user


class Team(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/')
    role = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    twitter = models.CharField(max_length=255)
    facebook = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='image/')

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True,)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True,)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True,)
    quantity = models.IntegerField(default=0, blank=True, null=True,)
    date_added = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True,)
    date_added = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.address
