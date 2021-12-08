from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, render
from .models import *
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from . import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def delivery(request):
    return render(request, 'store/coming_soon.html',)


def contact_us(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        contact.name = name
        contact.email = email
        contact.subject = subject
        contact.message = message
        contact.save()
        # send email
        send_mail(
            subject + "from" + name,
            message,
            email,
            ['festuskwafo11@gmail.com']
        )
        return render(request, 'store/contact_us.html')
    else:
        return render(request, 'store/contact_us.html')


def all_products(request):
    products = Product.objects.all().order_by('-id')[:5]
    featured = Product.objects.filter(is_featured=True)
    laptop = Product.objects.filter(category=1).order_by('-id')[:5]
    phones = Product.objects.filter(category=2).order_by('-id')[:2]
    return render(request, 'store/home.html', {'products': products, 'laptop': laptop, 'featured': featured, 'phones': phones})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    related_product = Product.objects.filter(
        category=product.category).exclude(slug=slug)
    return render(request, 'store/products/detail.html', {'product': product, 'related': related_product})


def about_us(request):
    teams = Team.objects.all()
    return render(request, "store/about_us.html", {'teams': teams})


def shop(request):
    products = Product.objects.all().order_by('-id')[:5]
    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)
    return render(request, 'store/shop.html', {'products': products, page: 'pages'})


def all_teams(request):
    teams = Team.objects.all()
    return render(request, 'store/about_us.html', {'teams': teams})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})


def services(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST['name']
        phonenum = request.POST['']
        email = request.POST['email']
        location = request.POST['subject']
        description = request.POST['message']
        contact.name = name
        contact.email = email
        contact.location = location
        contact.description = description
        contact.save()
        return render(request, 'store/services.html')
    else:
        return render(request, 'store/services.html')


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
    context = {'items': items}
    return render(request,  'store/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print("Action: ", action, "ProductId: ", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("Item was added", safe=False)
