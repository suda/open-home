from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import VendorSerializer, ProductSerializer, GroupSerializer, DeviceSerializer, CommandSerializer, UpdateSerializer
from .models import Vendor, Product, Group, Device, Command, Update


def index(request):
    return HttpResponse(u'Hello')

class SupportedVendorsViewSet(viewsets.ViewSet):
    queryset = Vendor.objects.all()

    def list(self, request):
        """
        Returns list of supported vendors
        """
        serializer = VendorSerializer(Vendor.objects.all())
        return Response(serializer.data)

class SupportedProductsViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()

    def list(self, request):
        return Response({u'error': u'Please provide Vendor to query'})

    def retrieve(self, request, pk):
        """
        Returns list of supported vendor products
        """
        vendor = get_object_or_404(Vendor, identifier=pk)
        serializer = ProductSerializer(vendor.product_set.all())
        return Response(serializer.data)

class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)

class DevicesViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (permissions.AllowAny,)

class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer
    permission_classes = (permissions.AllowAny,)

class UpdateViewSet(viewsets.ViewSet):
    queryset = Update.objects.all()

    def list(self, request):
        """
        Returns list of supported vendors
        """
        serializer = UpdateSerializer(Update.objects.order_by('-received_on'))
        return Response(serializer.data)