from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin

from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),

    url(r'^key/(\d+)', 'key.views.keyview'),
    url(r'^key/updatestate', 'key.views.updatestate'),
    url(r'^key/questionlist', 'key.views.questionlist'),
    url(r'^key/question/(\d+)', 'key.views.questionview'),
    url(r'^key/taxalist', 'key.views.taxalist'),

    url(r'^admin/', include(admin.site.urls)),
    
) 
