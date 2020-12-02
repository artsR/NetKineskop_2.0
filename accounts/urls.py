from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views



urlpatterns = [
    path('auth/login/', auth_views.LoginView.as_view(**settings.LOGIN_VIEW_CONFIG),
         name='login'),
    path('auth/register/', views.register, name='register'),
    path('authorize/', views.oauth_authorize, name='oauth_authorize'),
    path('callback/', views.oauth_callback, name='oauth_callback'),
    path('revoke/', views.oauth_revoke, name='oauth_revoke'),
    path('clear/', views.clear_credentials, name='oauth_credentials'),
]