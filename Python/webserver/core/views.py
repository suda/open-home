from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import parser_classes
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import VendorSerializer, ProductSerializer, GroupSerializer, DeviceSerializer, CommandSerializer, UpdateSerializer
from .models import Vendor, Product, Group, Device, Command, Update


def index(request):
    return HttpResponse(u'Hello')

class SupportedVendorViewSet(viewsets.ViewSet):
    queryset = Vendor.objects.all()

    def list(self, request):
        """
        Returns list of supported vendors
        """
        serializer = VendorSerializer(Vendor.objects.all())
        return Response(serializer.data)

class SupportedProductViewSet(viewsets.ViewSet):
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

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (permissions.AllowAny,)

class CommandViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CommandSerializer
    queryset = Command.objects.all()

    def list(self, request):
        """
        Returns list of supported vendors
        """
        serializer = CommandSerializer(Command.objects.order_by('-added_on'), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = CommandSerializer(data=request.DATA)
        if serializer.is_valid():
            command = serializer.object
            created = []
            if command.get('device'):
                # Send command to single device
                object = Command.objects.create(
                    device=command.get('device'),
                    kind=command.get('kind'),
                )
                serializer = CommandSerializer(object)
                created.append(serializer.data)
            else:
                # Send command to a group of devices
                for device in command.get('group').device_set.all():
                    object = Command.objects.create(
                        device=device,
                        kind=command.get('kind'),
                    )
                    serializer = CommandSerializer(object)
                    created.append(serializer.data)

            return Response(created, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateViewSet(viewsets.ViewSet):
    queryset = Update.objects.all()

    def list(self, request):
        """
        Returns list of supported vendors
        """
        serializer = UpdateSerializer(Update.objects.order_by('-received_on'))
        return Response(serializer.data)