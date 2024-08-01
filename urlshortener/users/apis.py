from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from urlshortener.users.models import BaseUser
from urlshortener.users.services import user_create
from urlshortener.users.validators import (
    letter_validator,
    number_validator,
    special_char_validator,
)


class UserCreateApi(APIView):
    class InputUserSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(
            required=True,
            validators=[
                MinLengthValidator(limit_value=8),
                number_validator,
                letter_validator,
                special_char_validator,
            ]
        )
        confirm_password = serializers.CharField(
            required=True,
            validators=[MinLengthValidator(limit_value=8)]
        )

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already taken.")
            return email
        
        def validate(self, attrs):
            if not attrs.get("password") or not attrs.get("confirm_password"):
                raise ValidationError("Password and confirm password are required.")
            
            if attrs.get("password") != attrs.get("confirm_password"):
                raise serializers.ValidationError("Password and confirm password must be equal.")
            
            return attrs

    class OutputUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("id", "email", "is_admin", "is_active")

    @extend_schema(request=InputUserSerializer, responses=OutputUserSerializer)
    def post(self, request):
        serializer = self.InputUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = user_create(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
            )
        except ValidationError:
            raise Response(
                data={"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        output_serializer = self.OutputUserSerializer(user)
        return Response(data=output_serializer.data, status=status.HTTP_201_CREATED) 
