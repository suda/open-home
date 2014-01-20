from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^cache\.manifest$', cache_manifest, name='cache_manifest'),
)


