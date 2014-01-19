import json
from rest_framework import serializers

class PayloadField(serializers.WritableField):
    """
    Field used to store additional data as JSON string in database
    """
    def to_native(self, value):
        if value == '':
            return None
        return json.loads(value)

    def from_native(self, value):
        # Just check if JSON is ok
        obj = json.loads(value)
        return value