from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterationSerializer, UserLoginSerializer
from rest_framework import permissions
from django.contrib.auth import login
from rest_framework import status
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()


class overview(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response("Hello")


class UserRegisteration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(request.data)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response("failed")


class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            user_data = User.objects.get(email=user.email)
            serialized_data = UserRegisterationSerializer(
                user_data
            )  # Just using the serializer to return important user data
            return Response(serialized_data.data, status=status.HTTP_200_OK)
