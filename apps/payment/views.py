#-*- coding:utf-8 -*-
# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from models import Order
from forms import OrderForm
from clothes.models import Clothes
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
import M2Crypto
import base64
from django.template.loader import render_to_string
from datetime import datetime
from kkb.tools import prepare_order as kkb_prepare_order
#from fakepay import prepare_order as fake_prepare_order
from django.shortcuts import get_object_or_404

def prep_order(request):
    if request.method == 'POST':
        form = OrderForm()
        variables = RequestContext(request, {
            'form': form,
            'product':Clothes.objects.get(id=request.POST['product_id'])
        })
        return render_to_response(
            'prepare_order.html',
            variables
        )
            
    else:
        raise Http404("Пожалуйста, покиньте эту страницу.")

def prepare_payment(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product = Clothes.objects.get(id=request.POST['product_id'])
            order = Order(
                buyer_id = request.user.id,
                address = form.cleaned_data['address'],
                phone = form.cleaned_data['phone'],
                email = request.user.email,
                amount = product.price,
                create_date = datetime.now(),
                payment_system = '11'
            )
            order.save()
            order.products.add(product)
            order.save()
            return HttpResponse(prepare_order('11', order.id, order.amount, order.phone, order.email))         
    else:
        raise Http404

    variables = RequestContext(request, {
        'form': form,
        'product': Clothes.objects.get(id=request.POST['product_id']),
    })
    return render_to_response(
        'prepare_order.html',
        variables
    )


def prepare_order(pay_sys_id, order_id, amount, phone, email):
    if pay_sys_id == '11':
        return kkb_prepare_order(order_id, amount, phone, email)
    #if pay_sys_id == '15':
    #    return fake_prepare_order(order_id, amount)

