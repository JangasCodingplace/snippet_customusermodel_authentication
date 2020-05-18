from django.urls import path

from . import open_api

urlpatterns = [
    path(
        'auth/login',
        open_api.login,
    ),
    path(
        'auth/create_user',
        open_api.create_user,
    ),
]