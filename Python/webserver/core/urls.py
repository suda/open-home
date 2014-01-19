from django.conf.urls import patterns, url, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'supported-vendor', SupportedVendorViewSet)
router.register(r'supported-product', SupportedProductViewSet)
router.register(r'group', GroupViewSet)
router.register(r'device', DeviceViewSet)
router.register(r'command', CommandViewSet)
router.register(r'update', UpdateViewSet)

urlpatterns = patterns('',
    url(r'^$', index, name='index'),

    url(r'^api/v1/', include(router.urls)),
)
