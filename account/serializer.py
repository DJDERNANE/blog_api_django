from django.contrib.auth.models import User
from rest_framework import serializers
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' ,'email', 'password', 'first_name', 'last_name']
        
        extra_kwargs = {
                'username': {'required': True, 'allow_blank': False, 'min_length' : 4 },
                'email': {'required': True, 'allow_blank': False },
                'password': {'required': True, 'allow_blank': False, 'min_length' :8 },
                'first_name': {'required': True, 'allow_blank': False },
                'last_name': {'required': True, 'allow_blank': False },
            }
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username' ,'email', 'first_name', 'last_name']
        