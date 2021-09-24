from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Activo API",
        default_version="v1",
        description="Asset Management Sytem",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-doc"),
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
]

admin.site.site_header = "Activo API"
admin.site.site_title = "Activo API Admin Portal"
admin.site.index_title = "Welcome to Activo Portal"
