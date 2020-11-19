from django.urls import path

from . import views



urlpatterns = [
    path('authorize/', views.oauth_authorize, name='oauth_authorize'),
    path('callback/', views.oauth_callback, name='oauth_callback'),
    path('revoke/', views.oauth_revoke, name='oauth_revoke'),
    path('clear/', views.clear_credentials, name='oauth_credentials'),
]