from django.conf.urls import patterns, include, url

from django.contrib import admin


urlpatterns = [
    url(r'', include(admin.site.urls)),
]
