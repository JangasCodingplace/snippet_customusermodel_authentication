import datetime
from django.conf import settings
from django.contrib import auth

from rest_framework import request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import User
from .serializers import BaseUserSerializer

@api_view(['POST',])
def login(request):
    if 'email' not in request.data or 'password' not in request.data:
        if request.session.session_key is None:
            data = {
                'err':'Missing request data'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = BaseUserSerializer(request.user)

        data = {
            'user':user_serializer.data
        }

        return Response(data, status=status.HTTP_202_ACCEPTED)


    # # #
    # Django default login

    user = auth.authenticate(
        request,
        email=request.data['email'],
        password=request.data['password']
    )

    if user is None:
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

@api_view(['POST',])
def create_user(request):
    required_props = [
        'first_name',
        'last_name',
        'email',
        'password'
    ]
    if [prop for prop in required_props if prop not in request.data]!=[]:
        data = {
            'err':'Missing request data'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=request.data['email']).exists():
        data = {
            'err':'User with that Email does already exist.'
        }
        return Response(data, status=status.HTTP_409_CONFLICT)
    
    user_serializer = BaseUserSerializer(data=request.data)
    if user_serializer.is_valid(raise_exception=True):
        new_user = user_serializer.save()
    
    auth.login(request._request, new_user)

    data = {
        'user':user_serializer.data
    }

    response = Response(data, status=status.HTTP_201_CREATED)

    # set session cookie
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

@api_view(['POST',])
def reset_password(request):
    if 'email' not in request.data:
        data = {
            'err':'Missing request data'
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({})
