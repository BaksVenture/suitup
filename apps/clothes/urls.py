from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'clothes.views.index'),
    url(r'^brand/(\d+)/$', 'clothes.views.brand_page'),
    url(r'^brand/catalog/(\d+)/$', 'clothes.views.brand_catalog'),
)
