import datetime
from django.contrib import auth
from django.conf import settings
from django.contrib.auth import update_session_auth_hash

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view

from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserSerializer,
    LoginUserSerializer
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


class ProfileLoginDataAPI(GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = LoginUserSerializer

    def put(self, request):
        if 'current_password' not in request.data:
            data = {
                'err':'Invalid request data'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


        if 'new_password' in request.data:
            if request.data['new_password'] != '':
                """
                password && email Change
                """
                if 'confirm_new_password' not in request.data:
                    data = {
                        'err':'Invalid request data'
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                if request.data['new_password'] != request.data['confirm_new_password']:
                    data = {
                        'err':'Password do not match!'
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
                request.data['password'] = request.data['new_password']
        

        user = auth.authenticate(
            request,
            email=request.user.email,
            password=request.data['current_password']
        )

        if user is None:
            data = {
                'err':'Wrong password'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        user_serializer = self.get_serializer(request.user, request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
        
        data = {}
        if request.data['new_password'] == '':
            return Response(data, status=status.HTTP_200_OK)

        update_session_auth_hash(request._request, user)

        response = Response(data, status=status.HTTP_200_OK)

        max_age = int(settings.ENV['SESSION_COOKIE_VALIDATION_TIME'])
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=max_age)
        response.set_cookie(
            key='sessionid',
            value=request.session.session_key,
            expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S UTC"),
            httponly=True,
            samesite='lax',
            path='/'
        )

        return response


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
