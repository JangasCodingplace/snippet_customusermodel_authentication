from django.contrib import auth

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view

from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserSerializer,
    ResetPWUserSerializer
)

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


class ProfilePasswordAPI(GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = ResetPWUserSerializer

    def post(self, request):
        if 'old_password' not in request.data or 'confirm_password' not in request.data:
            data = {
                'err':'Invalid request data'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        user = auth.authenticate(
            request,
            email=request.user.email,
            password=request.data['old_password']
        )

        if user is None:
            data = {
                'err':'Wrong password'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        
        if request.data['password'] != request.data['confirm_password']:
            data = {
                'err':'Passwords do not match'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = self.get_serializer(request.user, request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
        data = {}
        return Response(data, status=status.HTTP_200_OK)


class LogoutAPI(GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        User Logout
        """
        auth.logout(request._request)
        data = {}
        return Response(data, status=status.HTTP_200_OK)
