from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('index/', views.index, name='index'),

    path('registro-user/', views.register, name='register'),

    path('update-user/', views.update_user, name='update_user'),
    path('update-admin/<int:pk>/', views.update_admin, name='update_admin'),
    path('update-pass/', views.update_password, name='update_password'),
 
    path('user-list/', views.user_list, name='user_list'),
    path('user-delete/<int:pk>/', views.user_delete, name='user_delete'),
]
