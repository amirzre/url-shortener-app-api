from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from urlshortener.api.mixins import ApiAuthMixin
from urlshortener.users.selectors import user_get_login_data


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)
        return Response(data, status=status.HTTP_200_OK)
