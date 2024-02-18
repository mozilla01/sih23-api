from django.urls import path
from . import views

urlpatterns = [
    path("", views.Overview.as_view(), name="overview"),
    path("register/", views.UserRegisteration.as_view(), name="register"),
    path(
        "register-railway/",
        views.RailwayAccountRegisteration.as_view(),
        name="register-railway",
    ),
    path(
        "register-company/",
        views.CompanyAccountRegisteration.as_view(),
        name="register-company",
    ),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("get-rakes/", views.GetRakes.as_view(), name="get-rakes"),
    path("get-consumers/", views.GetConsumers.as_view(), name="get-consumers"),
    path("get-sources/", views.GetSources.as_view(), name="get-companies"),
    path("get-company/", views.GetCompany.as_view(), name="get-company"),
    path("get-railway/<str:pk>/", views.GetRailway.as_view(), name="get-railway"),
    path("get-client/<str:pk>/", views.GetClient.as_view(), name="get-client"),
    path("update-stock/", views.UpdateStock.as_view(), name="update-stock"),
    path("create-rake/", views.CreateRake.as_view(), name="create-rake")
]
