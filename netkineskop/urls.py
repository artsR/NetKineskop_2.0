from django.urls import path, re_path

from . import views



app_name = 'netkineskop'

urlpatterns = [
    re_path(r'^$|home/', views.home, name='home'),
    path('tags/', views.TagView.as_view(), name='tags'),
    path('tags/<int:pk>', views.DetailTagView.as_view(), name='detail_tag'),
    path('tags/<int:pk>/delete/', views.DeleteTagView.as_view(), name='delete_tag'),
    path('tags/<int:pk>/edit/', views.UpdateTagView.as_view(), name='update_tag'),
    path('add_tag/', views.AddTagView.as_view(), name='add_tag'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('videos/', views.videos, name='videos'),
]