from rest_framework import generics, permissions

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import User
from user.serializers import (
    CreateUserSerializer,
    UserSerializerWithToken,
    RetrieveUpdateUserSerializer
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = CreateUserSerializer


class ListProfilesUserView(generics.ListAPIView):
    """Retrieve all users"""
    serializer_class = RetrieveUpdateUserSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()


class ProfileUserView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete user profile"""
    serializer_class = RetrieveUpdateUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
