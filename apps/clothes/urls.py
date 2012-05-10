from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'clothes.views.index'),
    url(r'^brand/(\d+)/$', 'clothes.views.brand_page'),
    
)
