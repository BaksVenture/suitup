from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('registration.views',
    url(r'^login/$', 'login', name = "login"),
    url(r'^register/$', 'register', name = "register"),
    url(r'^logout/$', 'logout', name = 'logout'),
    url(r'^ajax_login/$', 'ajax_login', name = "login"),
    url(r'^ajax_register/$', 'ajax_register', name = "register"),
)

