from django.urls import path

from . import open_api
from . import intern_api

urlpatterns = [
    path(
        'auth/login',
        open_api.login,
    ),
    path(
        'auth/logout',
        intern_api.LogoutAPI.as_view(),
    ),
    path(
        'auth/create_user',
        open_api.create_user,
    ),
    path(
        'auth/reset_password',
        open_api.reset_password,
    ),
    path(
        '',
        intern_api.ProfileGeneralAPI.as_view(),
    ),
    path(
        'authdata_change',
        intern_api.ProfileLoginDataAPI.as_view(),
    ),
]