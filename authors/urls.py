from django.urls import path

from . import views





app_name = 'authors'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
]
