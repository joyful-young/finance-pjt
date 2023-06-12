
from django.contrib import admin
from django.urls import path
from . import views
from .views import max_intr_saving_products, kibon_intr_saving_products

app_name = 'saving'
urlpatterns = [
    
    path('save-saving-products/', views.save_saving_products),
    path('saving-products/', views.saving_products),
    path('saving-product-options/<str:fin_prdt_cd>/', views.saving_product_options),
    path('like_saving_product/<str:fin_prdt_cd>/', views.like_saving_product),
    path('register_saving_product/<str:fin_prdt_cd>/', views.register_saving_product),

    # 우대 금리 역순, 기준 금리 역순 정렬
    path('max_intr_saving_products/', max_intr_saving_products.as_view(), name='max_intr_deposit_products'),
    path('kibon_intr_saving_products/', kibon_intr_saving_products.as_view(), name='kibon_intr_deposit_products'),
    
    


]
