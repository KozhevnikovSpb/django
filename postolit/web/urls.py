from django.contrib import admin
from django.urls import path
from .views import index, reg, index_2, clickhouse_test, login

urlpatterns = [
    path('web/<int:id>', index_2),
    path('web', index, name="web"),
    path('reg', reg, name="reg"),
    path('click', clickhouse_test, name="click"),
    path('login', login, name="login")
]
