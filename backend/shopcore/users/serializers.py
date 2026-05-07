from rest_framework import serializers
from .models import CustomUser


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ['email', 'password']


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'first_name', 'last_name', 'salutation', 'date_of_birth', 'phone_number',
            'street_and_number', 'postal_code', 'city', 'country', 'password', 'is_staff', 'is_active',
            'is_superuser'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': False},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        # Überprüft, ob ein Passwort für die Erstellung erforderlich ist
        if not self.instance and not attrs.get('password'):
            raise serializers.ValidationError({"password": "Password is required for registration."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Passwort bleibt optional beim Update
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
