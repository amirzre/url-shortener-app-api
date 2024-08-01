from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from urlshortener.shortener.models import Shortner
from urlshortener.shortener.selectors import get_long_url
from urlshortener.shortener.services import create_or_get_short_url


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


class RedirectShortURLView(APIView):
    class InputRedirectSerializer(serializers.Serializer):
        short_url = serializers.CharField(required=True, max_length=2048)

    class OutputRedirectSerializer(serializers.Serializer):
        long_url = serializers.URLField()

    @extend_schema(
        request=InputRedirectSerializer,
        responses=OutputRedirectSerializer
    )
    def get(self, request, short_url):
        serializer = self.InputRedirectSerializer(data={"short_url": short_url})
        serializer.is_valid(raise_exception=True)

        try:
            long_url = get_long_url(short_url=serializer.validated_data.get("short_url"))
        except ObjectDoesNotExist:
            return Response({"detail": "Long URL not found."}, status=status.HTTP_404_NOT_FOUND)

        output_serializer = self.OutputRedirectSerializer(data={"long_url": long_url})
        output_serializer.is_valid(raise_exception=True)
        return Response(data=output_serializer.data, status=status.HTTP_200_OK)
