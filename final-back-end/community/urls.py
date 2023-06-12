
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'community'
urlpatterns = [
    # path('finlife/', include('finlife.urls')),
    
    path('' , views.article_list),
    path('article_like_list/', views.article_like_list),
    path('detail/<int:article_pk>/', views.article_detail),
    path('like/<int:article_pk>/', views.like_article),
    path('like_comments/<int:article_pk>/<int:comment_pk>/', views.like_comments),
    path('comment_create/<int:article_pk>/', views.comment_create),
    path('comment_detail/<int:comment_pk>/', views.comment_detail),
    # path('detail/', views.comment_list),
    
]
