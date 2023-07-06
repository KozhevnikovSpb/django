from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from web.models import User
from .serializers import UserSerializer


class UserView(APIView):
    authentication_classes = [TokenAuthentication] # Аутентифицируем пользователя по токену
    permission_classes = [IsAuthenticated] # Доступ только у атуентифицированных пользователей
    def get(self, request):
        objects = User.objects.all()
        serializer = UserSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
