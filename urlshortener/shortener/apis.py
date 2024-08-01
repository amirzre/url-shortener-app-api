from django.conf import settings
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from urlshortener.shortener.models import Shortner
from urlshortener.shortener.services import create_or_get_short_url


class ShortenerListApi(APIView):
    pass


class ShortenerDetailApi(APIView):
    class InputShortenerSerializer(serializers.Serializer):
        long_url = serializers.URLField(required=True, max_length=2048)

    class OutputShortenerSerializer(serializers.ModelSerializer):
        full_short_url = serializers.SerializerMethodField()

        class Meta:
            model = Shortner
            fields = ("short_url", "full_short_url")
        
        def get_full_short_url(self, obj):
            app_domain = settings.APP_DOMAIN
            return f"{app_domain}/{obj.short_url}"

    @extend_schema(request=InputShortenerSerializer, responses=OutputShortenerSerializer)
    def post(self, request):
        serializer = self.InputShortenerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            shortener, created = create_or_get_short_url(long_url=serializer.validated_data.get("long_url"))
        except ValidationError as ex:
            return Response({"detail": "error - " + str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        output_serializer = self.OutputShortenerSerializer(shortener)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
