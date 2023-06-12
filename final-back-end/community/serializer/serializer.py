from django.contrib.auth import get_user_model
from rest_framework import serializers
from community.models import Article, Comment
from accounts.models import User
# from accounts.serializers import UserSerializer

User = get_user_model()

# class CommentSerializer(serializers.ModelSerializer):
#     article = serializers.CharField( source='article.id')
#     user = serializers.CharField(source='user.username ') 
    
    
#     class Meta:
#         model = Comment
#         fields = ('id', 'content', 'created_at', 'updated_at', 'article', 'comment_like_user', 'user')
#         read_only_fields = ('created_at', 'updated_at', 'user')

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'comment_like_user', 'user', 'article', 'like_count')
    # class UserSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = User
    #         fields = ('id', 'username',)

    # class ArticleSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = Article
    #         fields = ('id',)

    
   
    # article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())
    # comment_like_user = serializers.PrimaryKeyRelatedField(many=True, read_only=True)






# 전체 게시글
class ArticleListSerializer(serializers.ModelSerializer):
    write_user = serializers.CharField(source='write_user.username')
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ('id', 'category', 'write_user', 'title', 'content', 'created_at', 'updated_at', 'comment_count', 'like_count')
    
    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_like_count(self, obj):
        return obj.article_like_user.count()


# 단일 게시글
class ArticleSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username',)


    liking_people = UserSerializer(many=True, read_only=True)

    write_user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


# 'write_user', 'comments', 

# class ArticleSerializer(serializers.ModelSerializer):

#     class UserSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = User
#             fields = 'identification'

#     class Meta:
#         model = Article

#         fields = '__all__'