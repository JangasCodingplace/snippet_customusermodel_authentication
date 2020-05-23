from django.urls import path

from . import api_extern
from . import api_intern

urlpatterns = [
    path(
        'auth/login',
        api_extern.login,
    ),
    path(
        'auth/logout',
        api_intern.LogoutAPI.as_view(),
    ),
    path(
        'auth/create_user',
        api_extern.create_user,
    ),
    path(
        'auth/reset_password',
        api_extern.reset_password,
    ),
    path(
        '',
        api_intern.ProfileGeneralAPI.as_view(),
    ),
    path(
        'authdata_change',
        api_intern.ProfileLoginDataAPI.as_view(),
    ),
]