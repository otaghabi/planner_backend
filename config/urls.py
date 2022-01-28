from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from config import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Planner API",
        default_version='v1',
        description="Planner API Document",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="plannerforuse@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

swagger_urlpatterns_debug = [
    re_path(r'^doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-redoc')
]

swagger_urlpatterns_production = [
    re_path(r'^doc/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-redoc')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/v1/', include('api.urls')),
]
urlpatterns += swagger_urlpatterns_production

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)