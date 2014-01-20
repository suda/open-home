import json
from rest_framework import serializers
from .fields import PayloadField
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

class CommandSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(many=False, queryset=Command.objects, read_only=True)
    added_on = serializers.DateTimeField(read_only=True)
    sent_on = serializers.DateTimeField(read_only=True)
    kind = serializers.IntegerField()
    kind_display = serializers.SerializerMethodField('get_kind_display')
    device = serializers.PrimaryKeyRelatedField(many=False, queryset=Device.objects, read_only=False, required=False)
    group = serializers.PrimaryKeyRelatedField(many=False, queryset=Group.objects, read_only=False, required=False, write_only=True)

    class Meta:
        fields = ('id', 'device', 'added_on', 'sent_on', 'kind', 'kind_display', 'group')

    def get_kind_display(self, obj):
        return '' if obj is None else None if not isinstance(obj, Command) else obj.get_kind_display()

    def validate_kind(self, attrs, source):
        value = attrs[source]
        if value is None or \
           value not in map(lambda kind: kind[0], Command.KIND_CHOICES):
            raise serializers.ValidationError('Invalid kind')

        return attrs
#
    def validate_device(self, attrs, source):
        value = attrs[source]
        if value is None and attrs.get('group') is None:
            raise serializers.ValidationError('Device or group required')

        return attrs

    def validate_group(self, attrs, source):
        value = attrs[source]
        if value is None and attrs.get('device') is None:
            raise serializers.ValidationError('Device or group required')

        return attrs

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