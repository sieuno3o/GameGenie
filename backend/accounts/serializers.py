from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'created_at', 'nickname']
        read_only_fields = ['created_at']

    def get_author(self, obj):
        return obj.username


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password])
    email = serializers.EmailField(required=False)
    profile_image = serializers.ImageField(source='profileImage', allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'nickname', 'profile_image']  # id 필드 추가
        read_only_fields = ['username']
