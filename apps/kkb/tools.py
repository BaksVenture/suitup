#-*-coding:utf-8-*-
from django.template.loader import render_to_string
from django.template import Context
from django.conf import settings
import M2Crypto
import base64
from django.contrib.sites.models import Site

def prepare_order(order_id, amount, phone, email):
    site = Site.objects.get_current()
    currency_id = "398"; 		# Шифр валюты  - 840-USD, 398-Tenge
    signed_order_b64 = process_request(order_id, currency_id, amount);
    variables = Context({
        'Signed_Order_B64': signed_order_b64,
        'AMOUNT': amount,
        'post_link': 'http://%s/kkb/postlink/' % site.domain,
        'back_link': 'http://%s/' % site.domain,
        'email': email,
        'phone': phone,
    })
    return render_to_string('kkb_payment.html', variables)


def get_passphrase(v = 0):
    return "nissan"


def process_request(order_id, currency_code, amount, b64 = True):
    pk = open(settings.PROJECT_PATH + '/apps/kkb/test_prv.pem', 'rb').read()
    signEVP = M2Crypto.EVP.load_key_string(pk, callback = get_passphrase)
    #rsa = M2Crypto.RSA.load_key_string(pk)
    #n, e = rsa.n, rsa.e

    config = {
        'MERCHANT_CERTIFICATE_ID': '00C182B189',
        'MERCHANT_NAME': 'Tartu.kz',
        'PRIVATE_KEY_FN': 'test_prv.pem',
        'PRIVATE_KEY_PASS': 'nissan',
        'XML_TEMPLATE_FN': 'template.xml',
        'XML_COMMAND_TEMPLATE_FN': 'command_template.xml',
        'PUBLIC_KEY_FN': 'kkbca.pem',
        'MERCHANT_ID': '92061101'
    }
    if len(str(order_id)) > 0:
        if order_id > 0:
            order_id = "%06d" % (order_id)
        else:
            return "Null Order ID"
    else:
        return "Empty Order ID"

    if len(str(currency_code)) == 0 :
        return "Empty Currency code"
    if amount == 0 :
        return "Nothing to charge"
    if len(config['PRIVATE_KEY_FN']) == 0:
        return "Path for Private key not found"
    if len(config['XML_TEMPLATE_FN']) == 0:
        return "Path for Private key not found"

    req = '<merchant cert_id="{{ MERCHANT_CERTIFICATE_ID }}" name="{{ MERCHANT_NAME }}"><order order_id="{{ ORDER_ID }}" amount="{{ AMOUNT }}" currency="{{ CURRENCY }}"><department merchant_id="{{ MERCHANT_ID }}" amount="{{ AMOUNT }}"/></order></merchant>'
    req = req.replace(
        '{{ MERCHANT_CERTIFICATE_ID }}',
        config['MERCHANT_CERTIFICATE_ID']
    )
    req = req.replace(
        '{{ MERCHANT_NAME }}',
        config['MERCHANT_NAME']
    )
    req = req.replace(
        '{{ ORDER_ID }}',
        order_id
    )
    req = req.replace(
        '{{ CURRENCY }}',
        currency_code
    )
    req = req.replace(
        '{{ MERCHANT_ID }}',
        config['MERCHANT_ID']
    )
    req = req.replace(
        '{{ AMOUNT }}',
        str(amount)
    )

    signEVP.sign_init()
    signEVP.sign_update(req)
    signature = signEVP.sign_final()
    signature = signature[::-1]
    #signature = rsa.sign(sha1(res).hexdigest())
    res_sign = '<merchant_sign type="RSA">' + base64.encodestring(signature) + '</merchant_sign>'
    xml = '<document>' + req + res_sign + '</document>'
    return base64.encodestring(xml)
