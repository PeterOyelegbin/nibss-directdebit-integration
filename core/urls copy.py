"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from accounts.views import *
from directdebit.views import *
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_spectacular.renderers import OpenApiYamlRenderer


urlpatterns = [
    # JSON Schema endpoint
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    
    # # YAML Schema endpoint (requires OpenAPIRenderer)
    # path('schema.yaml', SpectacularAPIView.as_view(renderer_classes=[OpenApiYamlRenderer]), name='schema-yaml'),
    
    # Swagger UI
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Redoc UI
    path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path("admin", admin.site.urls),

    # User authentication routes (API)
    path('api/v1/auth/login', LoginView.as_view(), name='user_login'),
    path('api/v1/auth/logout', LogoutView.as_view(), name='user_logout'),
    path('api/v1/auth/password/reset', PasswordResetView.as_view(), name='password_reset'),
    path('api/v1/auth/password/confirm', PasswordConfirmView.as_view(), name='password_confirm'),
    
    # User profile routes (API)
    path('api/v1/account/users', UserListCreateView.as_view(), name='users'),
    path('api/v1/account/users/<pk>', UserRetrUpdtDelView.as_view(), name='manage_users'),

    # Mandate routes (API)
    path('api/v1/mandates/create', CreateMandateView.as_view(), name='create_mandate'),
    path('api/v1/mandates/balance', BalanceEnquiryView.as_view(), name='mandate_balance'),
    path('api/v1/mandates/e-mandate', CreateEMandateView.as_view(), name='create_e_mandate'),
    path('api/v1/mandates/fetch/<str:page>/<str:pageSize>', FetchMandateView.as_view(), name='fetch_mandates'),
    path('api/v1/mandates/status', MandateStatusView.as_view(), name='mandate_status'),
    path('api/v1/mandates/update', UpdateMandateStatusView.as_view(), name='update_mandate_status'),
    
    # Biller routes (API)
    path('api/v1/biller/product/<int:billerID>', GetProductView.as_view(), name='get_product'),

    # Key request routes (API)
    path('api/v1/key', GetAPIKeyView.as_view(), name='get_key'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
