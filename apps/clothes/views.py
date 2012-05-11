from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, render, get_object_or_404
from models import Brand, Clothes, ClothesCategory
from registration.models import User as User2

def index(request):
    brands = Brand.objects.all();
    try:
        variables = RequestContext(request, {
            'brands': brands,
            'user': request.user,
            'user2': User2.objects.get(pk=request.user.id)
        })
    except User2.DoesNotExist:
        variables = RequestContext(request, {
            'brands': brands,
            'user': request.user,
        })
        
    return render_to_response('home.html', variables)
    
def brand_page(request, brand_id):
    return HttpResponse(str(brand_id))

def brand_catalog(request, brand_id):
    brand = get_object_or_404(Brand, pk = brand_id)
    clothes = Clothes.objects.filter(brand = brand)
    return render(request, "clothes/catalog.html", {'clothes': clothes, 'brand':brand})
    
def clothes_catalog(request, dress_type_id):
    dress_type = get_object_or_404(ClothesCategory, pk = dress_type_id)
    clothes = Clothes.objects.filter(dress_category=dress_type)
    return render(request, "clothes/catalog2.html", {'clothes': clothes, 'dress_type':dress_type})

def about(request):
    return render(request, "home.html", {'about': True})

def help(request):
    return render(request, "home.html", {'help': True})

def contacts(request):
    return render(request, "home.html", {'contacts': True})
