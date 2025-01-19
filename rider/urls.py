from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="rider API",
        default_version="v1",
        description="API Documentation for rider App",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="developer@enfono.co.in"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("api/admin/", admin.site.urls),
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0)),
    path("api/", include("api.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
