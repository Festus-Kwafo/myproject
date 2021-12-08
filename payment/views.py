from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse


from .models import *
from . import forms
# Create your views here.


# @login_required
# def BasketView(request):
#   return render(request, 'payment/make_payment.html')


def initiate_payment(request: HttpResponse) -> HttpResponse:
    if request.method == "POST":
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save()
            render(request, 'payment/make_payment.html', {'payment': payment})
    else:
        payment_form = forms.PaymentForm()
        render(request, 'payment/initiate_payment.html',
               {'payment_form': payment_form})
