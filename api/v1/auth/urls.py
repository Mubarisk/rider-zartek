from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RiderViewSet, DriverViewSet
from django.urls import path


urlpatterns = [
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("rider/register/", RiderViewSet.as_view({"post": "create"})),
    path(
        "rider/",
        RiderViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
    ),
    path("driver/register/", DriverViewSet.as_view({"post": "create"})),
    path(
        "driver/",
        DriverViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
    ),
]
