from django.urls import path
from .views import RideViewSet

urlpatterns = [
    path("rides/", RideViewSet.as_view({"get": "list", "post": "create"})),
    path("ride/<int:pk>/", RideViewSet.as_view({"patch": "update_status"})),
]
