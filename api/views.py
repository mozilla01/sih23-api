from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserRegisterationSerializer,
    UserLoginSerializer,
    RailwayAccountRegisterationSerializer,
    CompanyAccountRegisterationSerializer,
    RakeSerializer,
    ConsumerSerializer,
)
from rest_framework import permissions
from django.contrib.auth import login, logout
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import RailwayAccount, ConsumerAccount, CompanyAccount, Rake

# Create your views here.

User = get_user_model()


class Overview(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response("Hello")


class UserRegisteration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_serializer = UserRegisterationSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.create(request.data)
            return Response(data={"id": user.id}, status=status.HTTP_201_CREATED)
        else:
            print(user_serializer.errors)
            return Response(data="failed", status=status.HTTP_400_BAD_REQUEST)


class RailwayAccountRegisteration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        railway_serializer = RailwayAccountRegisterationSerializer(data=request.data)
        if railway_serializer.is_valid():
            railway_serializer.save()
            return Response(
                data=railway_serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            print(railway_serializer.errors)
            return Response("failed")


class CompanyAccountRegisteration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        company_serializer = CompanyAccountRegisterationSerializer(data=request.data)
        if company_serializer.is_valid():
            company_serializer.save()
            return Response(
                data=company_serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            print(company_serializer.errors)
            return Response(data="failed", status=status.HTTP_400_BAD_REQUEST)


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


class GetRakes(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        rakes = Rake.objects.all()
        serializer = RakeSerializer(rakes, many=True)
        return Response(serializer.data)


class GetConsumers(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        consumers = ConsumerAccount.objects.all()
        serializer = ConsumerSerializer(consumers, many=True)
        return Response(serializer.data)


class GetSources(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        sources = CompanyAccount.objects.all()
        serializer = CompanyAccountRegisterationSerializer(sources, many=True)
        return Response(serializer.data)


class GetCompany(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        company = CompanyAccount.objects.get(user=request.user)
        serializer = CompanyAccountRegisterationSerializer(company, many=False)
        return Response(serializer.data)


class GetRailway(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        railway = RailwayAccount.objects.get(id=pk)
        serializer = RailwayAccountRegisterationSerializer(railway, many=False)
        return Response(serializer.data)


class GetClient(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        client = ConsumerAccount.objects.get(id=pk)
        serializer = ConsumerSerializer(client, many=False)
        return Response(serializer.data)


class UpdateStock(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        source = CompanyAccount.objects.get(user=request.user)
        serializer = CompanyAccountRegisterationSerializer(
            instance=source, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(data="Stock updated", status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logout(request)
        return Response("User logged out")

class CreateRake(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RakeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(data="Rake not created", status=status.HTTP_400_BAD_REQUEST)
