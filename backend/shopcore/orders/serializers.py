from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'status', 'alternative_address', 'city', 'country', 'differentShippingAddress', 'email', 'first_name',
            'last_name', 'phone_number', 'postal_code', 'payedStatus', 'payed_at', 'paymentMethod', 'salutation',
            'selectedProducts', 'street_and_number', 'termsAccepted', 'totalPrice', 'orderPlacedByUserWithId',
            'stripe_session_id', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)

        order.save()

        return order
