from .views import account_profile,account_signup
from django.urls import path

urlpatterns=[path('accounts/profile/',account_profile,name="account_profile"),
             path('accounts/signup',account_signup,name='account_signup')]