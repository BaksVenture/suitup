# -*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from giftery.models import *
from payment.models import *


@csrf_exempt
def postlink_page(request):
    if request.method == 'POST':
        order = Order.objects.get(id = int(request.POST['order_id']))
        order.is_paid = True
        order.save()
        for gift in order.gifts.all():
            gift.pay(gift.nominal)
            gift.save()
        return HttpResponseRedirect('/accounts/profile/' + str(request.user.id) + '/')
    else:
        raise Http404
