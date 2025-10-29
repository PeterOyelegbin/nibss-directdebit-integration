from rest_framework import serializers
from django.core.validators import MinLengthValidator
from .models import UserModel, AuditLog


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[MinLengthValidator(6)], write_only=True)
    
    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'role', 'is_active']
        
    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'role', 'is_active']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    

class PasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(validators=[MinLengthValidator(6)])


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'details', 'created_at']
