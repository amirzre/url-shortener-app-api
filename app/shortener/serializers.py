import os

from django.conf import settings

from rest_framework import serializers

from core.models import ShortUrl


class ShortUrlField(serializers.Field):
    """
    Used to serialize a short id string, but to deserialize the short id with
    the base URL site included.
    """

    def to_representation(self, obj):
        """Deserializing"""
        return os.path.join(settings.SITE_URL, obj.short_id)

    def to_internal_value(self, short_id):
        """Serializing"""
        if not short_id:
            raise serializers.ValidationError('This field may not be blank.')
        if len(short_id) != ShortUrl.ID_LENGTH:
            raise serializers.ValidationError(
                f'This field has no more than {ShortUrl.ID_LENGTH} characters.'
            )

        return {'short_id': short_id}


class ShortUrlSerializer(serializers.ModelSerializer):
    """Creates short url object"""
    short_id = ShortUrlField(source='*', read_only=True)
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = ShortUrl
        fields = (
            'id', 'url', 'short_id', 'user', 'count', 'created', 'updated'
        )
        extra_kwargs = {
            'count': {'read_only': True},
        }

    def create(self, validated_data):
        """Overwrite method to use self.save() on the serializer directly."""
        return ShortUrl.objects.create(**validated_data)
