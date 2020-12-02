from django.urls import path, re_path

from . import views



app_name = 'netkineskop'

urlpatterns = [
    re_path(r'^$|home/', views.home, name='home'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('videos/', views.videos, name='videos'),
]