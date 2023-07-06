from django.contrib import admin
from django.urls import path
from .views import index, reg, index_2, clickhouse_test

urlpatterns = [
    path('web/<int:id>', index_2),
    path('web', index),
    path('reg', reg, name="reg"),
    path('click', clickhouse_test, name="click")
]
