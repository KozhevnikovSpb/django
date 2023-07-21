from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token # Для обычного токена
from rest_framework_simplejwt.views import TokenRefreshView # Для JWT-токена
from .views import UserView, JWTTokenObtainPairView

urlpatterns = [
    path('get_token/', obtain_auth_token, name="get_token"),
    path('users/', UserView.as_view(), name="users"), # адрес для получения JSON с пользователями

    path('get_jwt_token/', JWTTokenObtainPairView.as_view(), name="get_jwt_token"), # Получение токена (Для JWT-токена)
    path('refresh_jwt_token/', TokenRefreshView.as_view(), name="refresh_jwt_token"), # Обновление access токена (Для JWT)
]

