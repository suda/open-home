from django.conf.urls import patterns, url, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'supported_vendors', SupportedVendorsViewSet)
router.register(r'supported_products', SupportedProductsViewSet)
router.register(r'groups', GroupsViewSet)
router.register(r'devices', DevicesViewSet)
router.register(r'commands', CommandViewSet)
router.register(r'updates', UpdateViewSet)

urlpatterns = patterns('',
    url(r'^$', index, name='index'),

    url(r'^api/v1/', include(router.urls)),
)
