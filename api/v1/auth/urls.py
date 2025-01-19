from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RiderViewSet, DriverViewSet
from django.urls import path


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view()),
    path(
        "rider/register/",
        RiderViewSet.as_view({"post": "create"}),
        name="rider-register",
    ),
    path(
        "rider/",
        RiderViewSet.as_view({"get": "retrieve", "patch": "partial_update"}),
        name="rider",
    ),
    path(
        "driver/register/",
        DriverViewSet.as_view({"post": "create"}),
        name="driver-register",
    ),
    path(
        "driver/",
        DriverViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update"}, name="driver"
        ),
    ),
]
