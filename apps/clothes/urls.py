from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'clothes.views.index'),
    url(r'^brand/(\d+)/$', 'clothes.views.brand_page'),
    url(r'^brand/catalog/(\d+)/$', 'clothes.views.brand_catalog'),
    url(r'^type/(\d+)/$', 'clothes.views.clothes_catalog'),
    url(r'^help/$', 'clothes.views.help'),
    url(r'^about/$', 'clothes.views.about'),
    url(r'^contacts/$', 'clothes.views.contacts'),
)
