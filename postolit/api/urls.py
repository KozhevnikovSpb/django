from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserView

urlpatterns = [
    path('get_token/', obtain_auth_token, name="get_token"),
    path('users/', UserView.as_view(), name="users") # адрес для получения JSON с пользователями
]
