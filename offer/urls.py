from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:store_id>/', views.create_offer, name='create_offer'),
    path('update/<int:offer_id>/', views.update_offer, name='update_offer'),
    path('delete/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    path('shop/<int:store_id>/', views.shop_offers, name='shop_offers'),
    path('mall/<int:mall_id>/', views.mall_offers, name='mall_offers'),
    path('store/<int:store_id>/', views.store_offers, name='store_offers'),
]