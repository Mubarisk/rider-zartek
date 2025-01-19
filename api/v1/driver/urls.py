from django.urls import path
from .views import DriverRideViewSet

urlpatterns = [
    path("rides/", DriverRideViewSet.as_view({"get": "list"})),
    path(
        "ride/<int:pk>/", DriverRideViewSet.as_view({"patch": "update_status"})
    ),
    path("my-rides/", DriverRideViewSet.as_view({"get": "list_rides"})),
]
