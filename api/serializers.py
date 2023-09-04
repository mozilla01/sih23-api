from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.contrib.auth import authenticate

User = get_user_model()


class UserRegisterationSerializer(serializers.ModelSerializer):
    aadhaar = serializers.FileField(required=False)
    id_proof = serializers.FileField(required=False)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, clean_data):
        if clean_data["type"] == "railway":
            user = User.objects.create_user(
                password=clean_data["password"],
                email=clean_data["email"],
                type=clean_data["type"],
                division=clean_data["division"],
                pf_no=clean_data["pf_no"],
                operator_name=clean_data["operator_name"],
                contact_no=clean_data["contact_no"],
                org_contact_no=clean_data["org_contact_no"],
                aadhaar=clean_data.get("aadhaar", False),
                id_proof=clean_data.get("id_proof", False),
            )
            user.save()
        else:
            user = User.objects.create_user(
                password=clean_data["password"],
                email=clean_data["email"],
                type=clean_data["type"],
                company_name=clean_data["company_name"] or None,
                emp_position=clean_data["emp_position"],
                operator_name=clean_data["operator_name"],
                address=clean_data["address"],
                contact_no=clean_data["contact_no"],
                org_contact_no=clean_data["org_contact_no"],
                aadhaar=clean_data.get("aadhaar", False),
                id_proof=clean_data.get("id_proof", False),
            )
            user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, clean_data):
        user = authenticate(email=clean_data["email"], password=clean_data["password"])
        if not user:
            raise ValidationError("User not found")
        return user
