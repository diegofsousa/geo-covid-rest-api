"""geocovid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import routers
from .user import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="GeoCovid Rest API",
      default_version='v1',
      description="Uma API Rest de Geolocalização para áreas com concentração de infectação do vírus Covid-19.",
      #terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="diegofelima.ti@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('user/register/', include('geocovid.authorize.urls', namespace='authorize')),
    path('user/auth/', include('rest_auth.urls')),
    path('user/me/', views.Me.as_view()),
    path('health/', include('geocovid.health.urls', namespace='health')),
    path('admin/', admin.site.urls),
    path('docs', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

urlpatterns = [path('api/{}/'.format(settings.API_VERSION), include(urlpatterns))]
