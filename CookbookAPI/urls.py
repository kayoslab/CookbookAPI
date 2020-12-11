from django.urls import path, re_path
from django.conf.urls import include
from django.contrib import admin
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import config

swagger_info = openapi.Info(
    title="Cookbook API",
    default_version='v1',
    description="A RESTful API to provide recipe specific data",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@cr0ss.org"),
    license=openapi.License(name="BSD License"),
)

schema_view = get_schema_view(
    swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=config.API_URL,
)

@api_view(['GET'])
def plain_view(request):
    pass

def root_redirect(request):
    schema_view = 'schema-swagger-ui'
    return redirect(schema_view, permanent=True)

# urlpatterns required for settings values
required_urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns = [
    re_path(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('redoc-old/', schema_view.with_ui('redoc-old', cache_timeout=0), name='schema-redoc-old'),

    # re_path(r'^cached/swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='cschema-json'),
    # path('cached/swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='cschema-swagger-ui'),
    # path('cached/redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='cschema-redoc'),

    path('', root_redirect),
    path('cuisines/', include('cuisines.urls'), name='cuisines'),
    path('diets/', include('diets.urls'), name='diets'),
    path('ingredients/', include('ingredients.urls'), name='ingredients'),
    path('occasions/', include('occasions.urls'), name='occasions'),
    path('recipes/', include('recipes.urls'), name='recipes'),
] + required_urlpatterns
