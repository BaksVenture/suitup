from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from models import Brand

def index(request):
    brands = Brand.objects.all();
    variables = RequestContext(request, {
        'brands': brands,
        'user': request.user
    })
    return render_to_response('home.html', variables)
    
def brand_page(request, brand_id):
    return HttpResponse(str(brand_id))
