import json
from rest_framework import serializers
from core.fields import PayloadField
from .models import Vendor, Product, Group, Device, Command, Update


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('identifier', 'name', )

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('identifier', 'name', )

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', )

class CommandSerializer(serializers.ModelSerializer):
    kind_display = serializers.SerializerMethodField('get_kind_display')

    class Meta:
        model = Command
        fields = ('id', 'device', 'added_on', 'sent_on', 'kind', 'kind_display')
        read_only_fields = ('sent_on', )

    def get_kind_display(self, obj):
        return '' if obj is None else obj.get_kind_display()

class UpdateSerializer(serializers.ModelSerializer):
    kind_display = serializers.SerializerMethodField('get_kind_display')
    payload = PayloadField()

    class Meta:
        model = Update
        fields = ('id', 'device', 'received_on', 'payload', 'kind', 'kind_display' )

    def get_kind_display(self, obj):
        return '' if obj is None else obj.get_kind_display()

class DeviceSerializer(serializers.ModelSerializer):
    product_object = ProductSerializer(source='product', read_only=True)
    group_object = GroupSerializer(source='group', read_only=True)
    state_display = serializers.SerializerMethodField('get_state_display')
    payload = PayloadField()
    last_command = CommandSerializer(source='get_last_command', read_only=True)
    last_sent_command = CommandSerializer(source='get_last_sent_command', read_only=True)
    last_update = UpdateSerializer(source='get_last_update', read_only=True)

    class Meta:
        model = Device
        fields = ('id', 'product', 'product_object', 'group', 'group_object',
                  'name', 'state', 'state_display', 'payload', 'last_command',
                  'last_sent_command', 'last_update', )
        read_only_fields = ('state', )

    def get_state_display(self, obj):
        return '' if obj is None else obj.get_state_display()