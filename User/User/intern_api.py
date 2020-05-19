from django.contrib import auth

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer

class ProfileGeneralAPI(GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = UserSerializer

    def get(self, request):
        """
        Return Data related to UserObj
        """
        user_serializer = self.get_serializer(request.user)

        data = {
            'user':user_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    
    def put(self, request):
        """
        Modify Properties of UserObj
        """
        user_serializer = self.get_serializer(
            request.user,
            data=request.data
        )
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
        
        data = {
            'user':user_serializer.data
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)
    
    def post(self, request):
        """
        User Logout
        """
        auth.logout(request._request)
        data = {}
        return Response(data, status=status.HTTP_200_OK)
