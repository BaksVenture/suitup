#-*-coding:utf-8-*-
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import Context, RequestContext


def prepare_order(order_id, amount):
    variables = Context({
        'ORDER_ID': order_id,
        'AMOUNT': amount,
    })
    return render_to_response('fake_payment.html', variables)
