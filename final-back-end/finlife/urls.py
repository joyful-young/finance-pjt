
from django.contrib import admin
from django.urls import path
from . import views
from .views import max_intr_deposit_products, kibon_intr_deposit_products

appname = 'finlife'
urlpatterns = [
    path('save-deposit-products/', views.save_deposit_products ),
    path('deposit-products/', views.deposit_products),
    path('detail_deposit_product/<str:fin_prdt_cd>/', views.detail_deposit_product),
    path('like_deposit_product/<str:fin_prdt_cd>/', views.like_deposit_product),
    path('register_deposit_product/<str:fin_prdt_cd>/', views.register_deposit_product),
    
    # 어드민용 업데이트 옵션

    path('update_options/<int:id>/', views.update_options),

    # 우대 금리 역순, 기준 금리 역순 정렬
    path('max_intr_deposit_products/', max_intr_deposit_products.as_view(), name='max_intr_deposit_products'),
    path('kibon_intr_deposit_products/', kibon_intr_deposit_products.as_view(), name='kibon_intr_deposit_products'),
    
    
    
    # path('deposit-products/top_rate/', views.top_rate),
    # 상세인데 폐기
    # path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),
]
