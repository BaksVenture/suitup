from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404
from models import Brand, Clothes

def index(request):
    brands = Brand.objects.all();
    variables = RequestContext(request, {
        'brands': brands,
    })
    return render_to_response('home.html', variables)
    
def brand_page(request, brand_id):
    return HttpResponse(str(brand_id))

def brand_catalog(request, brand_id):
    brand = get_object_or_404(Brand, pk = brand_id)
    clothes = Clothes.objects.filter(brand = brand)
    return render(request, "clothes/catalog.html", {'clothes': clothes})
