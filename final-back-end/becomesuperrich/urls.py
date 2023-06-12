
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'becomesuperrich'
urlpatterns = [
    # path('finlife/', include('finlife.urls')),
    path('exam/', views.recommend_portfolio),
    # path('' , views.article_list),
    # path('', views.recommend, name='recommend'),
    
    # path('your_view/', views.your_view, name='recommend'),
    # 포트폴리오 에서 협업 필터링
    path('f_s_e/', views.collaborative_filtering_recommendation),

    # 예금 적금 협업 필터링
    path('recommend_unregistered_product/', views.recommend_unregistered_product),
    # 콘텐츠 필터링
    path('recommend_content_based/', views.recommend_content_based),
   
    path('hybrid_recommendation/', views.hybrid_recommendation),




]
