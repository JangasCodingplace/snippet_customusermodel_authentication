import datetime
from django.contrib import auth

from rest_framework import request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import BaseUserSerializer

@api_view(['POST',])
def login(request):
    if 'email' not in request.data or 'password' not in request.data:
        data = {
            'err':'Missing request data'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


    # # #
    # Django default login

    user = auth.authenticate(
        request,
        email=request.data['email'],
        password=request.data['password']
    )

    if not user:
        data = {
            'err':'User does not exist or wrong password.'
        }
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    
    auth.login(request._request, user)

    # ./Django default login
    # # #


    user_serializer = BaseUserSerializer(user)

    data = {
        'user':user_serializer.data
    }

    response = Response(data, status=status.HTTP_202_ACCEPTED)

    # set session cookie
    max_age = 365 * 24 * 60 * 60
    expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
    response.set_cookie(
        key='sessionid',
        value=request.session.session_key,
        expires=expires.strftime("%a, %d-%b-%Y %H:%M:%S UTC"),
        httponly=True,
        samesite='lax',
        path='/'
    )

    return response
