from django.urls import path
from . import views

urlpatterns = [
    path('create_store/<int:mall_id>/', views.create_store, name='create_store'),
    path('store_list/<int:mall_id>/', views.store_list, name='store_list'),
    path('update_store/<int:store_id>/', views.update_store, name='update_store'),
    path('delete_store/<int:store_id>/', views.delete_store, name='delete_store'),
    path('shop_login/', views.shop_login, name='shop_login'),
    path('shop_dashboard/', views.shop_dashboard, name='shop_dashboard'),
    path('store_logout/', views.store_logout, name='store_logout'),
    path('shop_list/<int:mall_id>/', views.shop_list, name='shop_list'),
    path('shop/<int:shop_id>/products/', views.customer_product_list, name='customer_product_list'),

]