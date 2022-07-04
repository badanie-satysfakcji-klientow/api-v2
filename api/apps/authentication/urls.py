from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.AuthenticationViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', views.AuthenticationViewSet.as_view({'get': 'logout'}), name='logout'),
    path('register/', views.AuthenticationViewSet.as_view({'post': 'register'}), name='register'),
    path('reset-password/', views.AuthenticationViewSet.as_view({'patch': 'reset_password'}), name='reset-password'),
]