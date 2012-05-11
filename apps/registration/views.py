from django.http import HttpResponse, Http404
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template, RequestContext, Context
from django.contrib.auth.models import User
from registration.models import User as User2

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
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
    
def ajax_login(request):
    username = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        variables = Context({'user': user})
        t = Template("hello {{ user.username }} | <a href=\"javascript:ajax_logout();\">logout</a>")
        return HttpResponse(t.render(variables))
    else:
        return HttpResponse("{{{FAIL}}}")
    

def ajax_register(request):

    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(username=username)
            return HttpResponse("{{{USERNAME}}}")
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=email)
                return HttpResponse("{{{EMAIL}}}")
            except User.DoesNotExist:
                user = User.objects.create_user(username=username,email=email,password=password)

        user.save()
        user2 = User2.objects.create(user=user)
        user2.save()
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            variables = Context({'user': user})
            t = Template("hello {{ user.username }} | <a href=\"javascript:ajax_logout();\">logout</a>")
            return HttpResponse(t.render(variables))
   
    return HttpResponse("FAIL")
