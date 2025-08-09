from rest_framework import serializers
from .models import User  # Adjust if your user model import is different

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name','avatar']  # Add username or any field you like
        read_only_fields = ['id', 'email','avatar']
