from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

from core.models import ShortUrl
from shortener.serializers import ShortUrlSerializer


class ShortenUrl(CreateAPIView):
    """Create shorten a URL"""
    serializer_class = ShortUrlSerializer

    def post(self, request):
        data = {
            'url': request.data.get('url'),
            'short_id': ShortUrl.generate_short_id(),
        }

        serializer = ShortUrlSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            if request.user.is_authenticated:
                serializer.save(user=self.request.user)
            else:
                serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetOrginalUrl(APIView):
    """Decode a URL short id into a the original URL"""

    def get(self, request, short_id):
        try:
            obj = ShortUrl.objects.get(short_id=short_id)
            obj.increase_short_id_counter()
            self.url = obj.url
            return redirect(self.url)

        except ObjectDoesNotExist:
            return Response(
                {'error': 'Short url id does not exist!'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ShortUrlList(ListAPIView):
    """Lists of all urls"""
    serializer_class = ShortUrlSerializer
    permission_classes = (IsAdminUser,)
    queryset = ShortUrl.objects.all()


class RetrieveShortUrl(RetrieveUpdateDestroyAPIView):
    """Retrieve a short url"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ShortUrlSerializer
    queryset = ShortUrl.objects.all()
