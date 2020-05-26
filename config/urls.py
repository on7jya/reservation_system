from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi

from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Test app API",
        default_version='v1',
        description="API for menu",
        terms_of_service="https://www.example.com/",
        contact=openapi.Contact(email="Ivan.Kataev@x5.ru;Igor.Kiselev@x5.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r"^swagger/$", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r"^redoc/$", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/user/", include("apps.users.urls", namespace="users")),
    path("api/", include("apps.rooms.urls", namespace="rooms")),
    path("api/reservation/", include("apps.reservation.urls", namespace="reservation")),
    path('sentry-debug/', trigger_error),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
