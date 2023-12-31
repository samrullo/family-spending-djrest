"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include

from dj_rest_auth.registration.views import VerifyEmailView,ConfirmEmailView,ResendEmailVerificationView
from dj_rest_auth.views import LoginView,LogoutView

from rest_framework.response import Response
from family_spending.basic_views import base_view


urlpatterns = [
    path('',include('users.urls')),
    path('api/v1/',include('family_spending.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),    
    path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/v1/dj-rest-auth/registration', include('dj_rest_auth.registration.urls')),
    path('api/v1/dj-rest-auth/registration/verify-email/', VerifyEmailView.as_view(), name='account_email'),
    path('api/v1/dj-rest-auth/registration/verify-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('api/v1/dj-rest-auth/registration/resend-email',ResendEmailVerificationView.as_view(),name="resend_email"),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('',base_view,name="base_view"),
    
]
