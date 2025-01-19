from django.urls import path, include


urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("rider/", include("api.v1.rider.urls")),
    path("driver/", include("api.v1.driver.urls")),
]
