from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.mall_login, name='mall_login'),
    path('dashboard/', views.mall_dashboard, name='mall_dashboard'),
    path('logout/', views.mall_logout, name='mall_logout'),
    path('list/', views.mall_list, name='mall_list'),


]