from django.urls import path , include
from django.conf import settings
from . import views


app_name = 'accounts'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('update-user/', views.update_user, name='update_user'),
    path('update-pass/', views.update_password, name='update_password'),
    path('registro-user/', views.register, name='register'),
]
  


  