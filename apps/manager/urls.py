from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('manager.views',
    url(r'^$', 'index', name = "manager_index"),
    url(r'^login/$', 'login', name = "manager_login"),
    url(r'^logout/$', 'logout', name = 'manager_logout'),
    url(r'^clothes/$', 'clothes', name = 'manager_clothes'),
    url(r'^add/$', 'add', name = 'manager_add'),
    url(r'^settings/$', 'settings', name = 'manager_settings'),
    url(r'^delete/(\d+)/$', 'delete', name = 'manager_delete'),
    url(r'^edit/(\d+)/$', 'edit', name = 'manager_edit'),
)

