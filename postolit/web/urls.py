from django.contrib import admin
from django.urls import path
from .views import index, reg, index_2, clickhouse_test, login_view, logout_view, anonymous_page, anonymous_session


urlpatterns = [
    path('web/<int:id>', index_2),
    path('web', index, name="web"),
    path('reg', reg, name="reg"),
    path('click', clickhouse_test, name="click"),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),
    path('anonymous_session', anonymous_session, name="anonymous_session"),
    path('anonymous_page', anonymous_page, name="anonymous_session")
]