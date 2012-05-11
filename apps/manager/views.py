from django.http import HttpResponse, Http404
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import Template, RequestContext, Context
from django.contrib.auth.models import User
from clothes.models import Brand, Clothes
from django.db.models import Q
from forms import ClothesForm, BrandForm

def index(request):
    if request.user.is_authenticated() and request.user.is_staff:
        brand = Brand.objects.filter(manager=request.user)
        return render(request, "manager/text.html", {'brand':brand})
    else:
        return render(request, "manager/login.html", {'':''})

def login(request):
    username = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active and user.is_staff:
        auth.login(request, user)
        return HttpResponseRedirect("/manager/")
    else:
        return HttpResponse("Error occured, wrong login or password")
        
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def clothes(request):
    b = Brand.objects.filter(manager=request.user)[0:1].get()
    clothes = Clothes.objects.filter(brand=b)
    return render(request, "manager/table.html", {'clothes':clothes})

def add(request):
    if request.method == "POST":
        form = ClothesForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/manager/clothes/")
    else:
        form = ClothesForm()
    return render(request, "manager/form.html", {'form':form})

def edit(request, id):
    item = get_object_or_404(Clothes, pk = id)
    if request.method == "POST":
        form = ClothesForm(request.POST, request.FILES, instance = item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/manager/clothes/")
    else:
        form = ClothesForm(instance = item)
    return render(request, "manager/form.html", {'form':form})

def delete(request, id):
    item = get_object_or_404(Clothes, pk = id)
    item.delete()
    return HttpResponseRedirect("/manager/clothes/")

def settings(request):
    brand = Brand.objects.filter(manager=request.user)[0:1].get()
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES, instance = brand)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/manager/")
    else:
        form = BrandForm(instance = brand)
    return render(request, "manager/settings.html", {'form':form})

