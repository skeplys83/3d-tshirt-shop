from rest_framework import serializers
from .models import Product
import base64


class Base64BinaryField(serializers.Field):
    def to_internal_value(self, data):
        # Prüfe, ob die Eingabe als Base64-String kommt
        if not isinstance(data, str):
            raise serializers.ValidationError("Expected a base64 encoded string")

        # Versuche, die Base64-Daten zu dekodieren
        try:
            decoded_data = base64.b64decode(data)
            return decoded_data
        except Exception as e:
            raise serializers.ValidationError("Invalid Base64 encoding")

    def to_representation(self, value):
        # Encodiert Binärdaten als Base64-String für die Ausgabe
        if value:
            return base64.b64encode(value).decode('utf-8')
        return None


class ProductSerializer(serializers.ModelSerializer):
    productPicture = Base64BinaryField(required=False, allow_null=True)
    productBlenderModel = Base64BinaryField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stripePriceId', 'stock', 'created_at',
            'updated_at', 'productBlenderModel', 'productPicture', 'colors', 'category',
            'discount', 'discountInPercent'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        if not self.instance:
            if 'stock' not in attrs or not attrs['stock']:
                raise serializers.ValidationError({"stock": "Stock is required for creating a product."})
            if 'colors' not in attrs or not attrs['colors']:
                raise serializers.ValidationError({"colors": "Colors are required for creating a product."})
            if 'stripePriceId' not in attrs or not attrs['stripePriceId']:
                raise serializers.ValidationError(
                    {"stripePriceId": "stripePriceId is required for creating a product."})
        return attrs
