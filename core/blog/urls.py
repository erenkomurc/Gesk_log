from django.urls import path
from .views import RemoteClient
from .import views


urlpatterns = [
     path('remote/', views.RemoteClient, name='remote.html'),
     path('remote/<str:selected_gw_id>', views.RemoteClient, name='remote.html'),
     path('replaces/', views.ReplaceClient, name='replaces.html'),

   
]
