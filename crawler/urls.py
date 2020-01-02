from django.conf.urls import url
from django.contrib import admin

from crawler import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^files/$', views.files, name='files'),
    url(r'^files/(?P<id>[0-9]+)$', views.file_info, name='file_info'),
    url(r'^urls/$', views.urls, name='urls'),
    url(r'^success/$', views.success, name='success'),
    url(r'^error/$', views.error, name='error'),
]
