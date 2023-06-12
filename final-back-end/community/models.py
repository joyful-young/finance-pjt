from django.db import models
from django.conf import settings


# Create your models here.
# 말머리 필드 지정하기 주식, 채권, 예금, 적금, 대출 제한해놓기 

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # 말머리
    category = models.CharField(max_length=100) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 익명 여부 넣어야 함
    annoymous_is_active = models.BooleanField(default=False)
    
    # 글 쓴 유저
    write_user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name='articles',)

    # 게시글에 좋아요 한 유저
    article_like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles' , blank=True )
    
    like_count = models.PositiveIntegerField(default=0)



class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users_comments')
    

    # 댓글 달린 게시글
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    # 댓글을 좋아요 한 유저
    comment_like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments' , blank=True )
    
    like_count = models.PositiveIntegerField(default=0)


