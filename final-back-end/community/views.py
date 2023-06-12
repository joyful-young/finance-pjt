from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authentication import TokenAuthentication
# Authentication Decorators
# from rest_framework.decorators import authentication_classes

# permission Decorators
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializer.serializer import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Article, Comment
from django.db.models import Count





# 전체 게시글 조회 및 게시글 생성
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능

def article_list(request):
    if request.method == 'GET':
        # articles = Article.objects.all()
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(write_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)








# @permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
# @authentication_classes([TokenAuthentication])

# 단일 게시글 조회, 삭제, 수정
@api_view(['GET', 'DELETE', 'PUT'])
# @authentication_classes([AllowAny])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    
    
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        data = serializer.data
        try:
            article.article_like_user.get(id=request.user.id)
            data['like_flag'] = True
        except:
            data['like_flag'] = False

        return Response(data)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)


        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

# 게시글 좋아요 순 정렬
@api_view(['GET'])
@permission_classes([AllowAny])
def article_like_list(request):
    if request.method == 'GET':
        articles = Article.objects.annotate(like_count_annotation=Count('article_like_user')).order_by('-like_count_annotation')
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)









@api_view(['GET'])
def comment_list(request):
    if request.method == 'GET':
        # comments = Comment.objects.all()
        comments = get_list_or_404(Comment)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    # comment = Comment.objects.get(pk=comment_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    

# 댓글 생성
@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_create(request, article_pk):
    
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article, user=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comments(request, article_pk, comment_pk):
    # 일단 아티클 쓸 일 없어서 주석처리
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    # 
    user = request.user

    if user in comment.comment_like_user.all():
        comment.comment_like_user.remove(user)
        # 추후 필드로 변경 좋아요 수
        like_count = comment.comment_like_user.count()

    else:
        # 좋아요
        comment.comment_like_user.add(user)
        like_count = comment.comment_like_user.count()

    # 좋아요 수
    comment.save()
    data = {
        "like_count" : like_count,
    }

    return Response(data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_article(request, article_pk):
    article = get_object_or_404(Article, id=article_pk)

    # 
    user = request.user

    if user in article.article_like_user.all():
        # 좋아요 취소
        article.article_like_user.remove(user)
        article.like_count -= 1
    else:
        # 좋아요
        article.article_like_user.add(user)
        article.like_count += 1

    # 좋아요 수
    article.save()
    data = {
        "like_count" : article.like_count,
    }

    return Response(data)