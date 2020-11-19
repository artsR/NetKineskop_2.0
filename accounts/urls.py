from django.urls import path

from . import views



urlpatterns = [
    path('authorize/', views.oauth_authorize),
    path('callback/', views.oauth_callback),
    path('revoke/', views.oauth_revoke),
    path('clear/', views.clear_credentials),
]