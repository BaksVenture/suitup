from django.conf.urls.defaults import patterns, url
from views import postlink_page, postlink_test_page


urlpatterns = patterns('',
    url(r'^postlink/$', postlink_page),
    url(r'^postlink/test/$', postlink_test_page),
)
