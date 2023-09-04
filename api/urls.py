from django.urls import path
from . import views

urlpatterns = [
    path("", views.overview.as_view(), name="overview"),
    path("register/", views.UserRegisteration.as_view(), name="register"),
    path("login/", views.UserLogin.as_view(), name="login"),
]
