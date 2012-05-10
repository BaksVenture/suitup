from django.http import HttpResponse, Http404
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

def login(request):
    username = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/account/invalid/")

def register(request):

    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        return HttpResponseRedirect("/")
   
    return HttpResponseRedirect("/account/invalid/")
