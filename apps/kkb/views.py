#-*- coding:utf-8 -*-
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from xml.dom import minidom
from django.utils.html import strip_tags
import base64
from django.views.decorators.csrf import csrf_exempt
import M2Crypto
from django.conf import settings
from giftery.models import *
from payment.models import *


@csrf_exempt
def postlink_page(request):
    if request.method == 'POST':
        response = request.POST['response'].decode('string_escape')
        xml_dict = parse_xml(response)
        rawsign = base64.decodestring(xml_dict['RAWSIGN'])[::-1]
        pk = open(settings.PROJECT_PATH + '/apps/kkb/kkbca.pem', 'rb').read()
        pubkey = M2Crypto.X509.load_cert_string(pk).get_pubkey()
        pubkey.verify_init()
        pubkey.verify_update(xml_dict['LETTER'])
        check_sign = pubkey.verify_final(rawsign)
        if check_sign:
            order = Order.objects.get(id = int(xml_dict['ORDER_ORDER_ID']))
            order.is_paid = True
            order.save()
            for gift in order.gifts.all():
                gift.pay(int(gift.certificate.nominal))
                gift.save()
            return HttpResponseRedirect('/accounts/profile/' + str(request.user.id) + '/')
        else:
            raise Http404
    else:
        raise Http404


def postlink_test_page(request):
    variables = RequestContext(request)
    return render_to_response('postlink_test.html', variables)


def parse_xml(xml):
    html = ''
    dom = minidom.parseString(xml)
    bank = dom.getElementsByTagName("bank")[0]
    customer = dom.getElementsByTagName("customer")[0]
    merchant = dom.getElementsByTagName("merchant")[0]
    order = dom.getElementsByTagName("order")[0]
    department = dom.getElementsByTagName("department")[0]
    merchant_sign = dom.getElementsByTagName("merchant_sign")[0]
    customer_sign = dom.getElementsByTagName("customer_sign")[0]
    results = dom.getElementsByTagName("results")[0]
    payment = dom.getElementsByTagName("payment")[0]
    bank_sign = dom.getElementsByTagName("bank_sign")[0]

    letter = '<bank ' + xml.split('<bank ')[1].split('</bank>')[0] + '</bank>'

    html += 'BANK_NAME = ' + bank.getAttribute('name') + '<br />'
    html += 'CUSTOMER_NAME = ' + customer.getAttribute('name') + '<br />'
    html += 'CUSTOMER_MAIL = ' + customer.getAttribute('mail') + '<br />'
    html += 'CUSTOMER_PHONE = ' + customer.getAttribute('phone') + '<br />'
    html += 'MERCHANT_CERT_ID = ' + merchant.getAttribute('cert_id') + '<br />'
    html += 'MERCHANT_NAME = ' + merchant.getAttribute('name') + '<br />'
    html += 'ORDER_ORDER_ID = ' + order.getAttribute('order_id') + '<br />'
    html += 'ORDER_AMOUNT = ' + order.getAttribute('amount') + '<br />'
    html += 'ORDER_CURRENCY = ' + order.getAttribute('currency') + '<br />'
    html += 'DEPARTMENT_MERCHANT_ID = ' + department.getAttribute('merchant_id') + '<br />'
    html += 'DEPARTMENT_AMOUNT = ' + department.getAttribute('amount') + '<br />'
    html += 'MERCHANT_SIGN_TYPE = ' + merchant_sign.getAttribute('type') + '<br />'
    html += 'CUSTOMER_SIGN_TYPE = ' + customer_sign.getAttribute('type') + '<br />'
    html += 'RESULTS_TIMESTAMP = ' + results.getAttribute('timestamp') + '<br />'
    html += 'PAYMENT_MERCHANT_ID = ' + payment.getAttribute('merchant_id') + '<br />'
    html += 'PAYMENT_AMOUNT = ' + payment.getAttribute('amount') + '<br />'
    html += 'PAYMENT_REFERENCE = ' + payment.getAttribute('reference') + '<br />'
    html += 'PAYMENT_APPROVAL_CODE = ' + payment.getAttribute('approval_code') + '<br />'
    html += 'PAYMENT_RESPONSE_CODE = ' + payment.getAttribute('response_code') + '<br />'
    html += 'BANK_SIGN_CERT_ID = ' + bank_sign.getAttribute('cert_id') + '<br />'
    html += 'BANK_SIGN_TYPE = ' + bank_sign.getAttribute('type') + '<br />'
    html += 'SIGN = ' + strip_tags(bank_sign.toxml()) + '<br / >'

    parsed_xml = {
        'BANK_NAME': bank.getAttribute('name'),
        'CUSTOMER_NAME': customer.getAttribute('name'),
        'CUSTOMER_MAIL': customer.getAttribute('mail'),
        'CUSTOMER_PHONE': customer.getAttribute('phone'),
        'MERCHANT_CERT_ID': merchant.getAttribute('cert_id'),
        'MERCHANT_NAME': merchant.getAttribute('name'),
        'ORDER_ORDER_ID': order.getAttribute('order_id'),
        'ORDER_AMOUNT': order.getAttribute('amount'),
        'ORDER_CURRENCY': order.getAttribute('currency'),
        'DEPARTMENT_MERCHANT_ID': department.getAttribute('merchant_id'),
        'DEPARTMENT_AMOUNT': department.getAttribute('amount'),
        'MERCHANT_SIGN_TYPE': merchant_sign.getAttribute('type'),
        'CUSTOMER_SIGN_TYPE': customer_sign.getAttribute('type'),
        'RESULTS_TIMESTAMP': results.getAttribute('timestamp'),
        'PAYMENT_MERCHANT_ID': payment.getAttribute('merchant_id'),
        'PAYMENT_AMOUNT': payment.getAttribute('amount'),
        'PAYMENT_REFERENCE': payment.getAttribute('reference'),
        'PAYMENT_APPROVAL_CODE': payment.getAttribute('approval_code'),
        'PAYMENT_RESPONSE_CODE': payment.getAttribute('response_code'),
        'BANK_SIGN_CERT_ID': bank_sign.getAttribute('cert_id'),
        'BANK_SIGN_TYPE': bank_sign.getAttribute('type'),
        'SIGN': bank_sign.toxml(),
        'RAWSIGN': strip_tags(bank_sign.toxml()),
        'LETTER': letter,
    }


    return parsed_xml
