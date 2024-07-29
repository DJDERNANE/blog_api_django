from django.shortcuts import render
from account.serializer import SignUpSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
# Create your views here.


@api_view(['POST'])
def signUp(request):
    data = request.data
    serializer = SignUpSerializer(data = data)
    if serializer.is_valid():
        username = data['username']
        email = data['email']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        # Check if user already exists
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        # Hash the password
        hashed_password = make_password(password)
        # Create a new user
        user = User.objects.create(username=username, email=email, password=hashed_password, first_name=first_name, last_name = last_name)
        userSerializer = UserSerializer(user)
        return Response(userSerializer.data, status.HTTP_201_CREATED)
    else :
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)