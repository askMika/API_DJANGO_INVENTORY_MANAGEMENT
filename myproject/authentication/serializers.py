from rest_framework import serializers
#from django.contrib.auth.models import User
from .models import User

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role','last_name','first_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            first_name=validated_data.get('first_name',''),
            last_name=validated_data.get('last_name','')
        )

        return user