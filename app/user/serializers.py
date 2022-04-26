from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for create user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validate_data):
        """Create a new user"""
        return get_user_model().objects.create_user(**validate_data)

    def update(self, instance, validate_data):
        """Update a user, setting the password correctly and return it"""
        password = validate_data.pop('password', None)
        user = super().update(instance, validate_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserSerializerWithToken(CreateUserSerializer):
    """Serializer for create user object with token"""
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'token', 'id', 'email', 'name',
            'is_active', 'is_staff', 'is_superuser',
        )

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class RetrieveUpdateUserSerializer(serializers.ModelSerializer):
    """Serializer for the user authentication object"""

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'email', 'password', 'name', 'is_active',
            'is_superuser', 'is_staff',
        )
        extra_kwargs = {'id': {'read_only': True}}
