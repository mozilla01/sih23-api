from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.contrib.auth import authenticate
from users.models import RailwayAccount, CompanyAccount, ConsumerAccount, Rake

User = get_user_model()


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerAccount

        fields = "__all__"


class RakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rake
        fields = "__all__"


class UserRegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, clean_data):
        user = User.objects.create_user(
            password=clean_data["password"],
            email=clean_data["email"],
            type=clean_data["type"],
        )
        user.save()
        return user


class RailwayAccountRegisterationSerializer(serializers.ModelSerializer):
    aadhaar = serializers.FileField(required=False)
    id_proof = serializers.FileField(required=False)

    class Meta:
        model = RailwayAccount
        fields = "__all__"


class CompanyAccountRegisterationSerializer(serializers.ModelSerializer):
    aadhaar = serializers.FileField(required=False)
    corporation_proof = serializers.FileField(required=False)

    class Meta:
        model = CompanyAccount
        fields = "__all__"


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(email=clean_data["email"], password=clean_data["password"])
        if not user:
            raise ValidationError("User not found")
        return user
