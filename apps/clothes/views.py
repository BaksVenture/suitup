from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response

def index(request):
    variables = RequestContext(request)
    return render_to_response('home.html', variables)
