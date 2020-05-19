from django.urls import path

from . import open_api
from . import intern_api

urlpatterns = [
    path(
        'auth/login',
        open_api.login,
    ),
    path(
        'auth/create_user',
        open_api.create_user,
    ),
    path(
        '',
        intern_api.ProfileGeneralAPI.as_view()
    )
]