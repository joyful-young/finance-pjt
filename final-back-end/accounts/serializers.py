from .models import User, Profile
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from community.models import Article, Comment
from finlife.models import DepositProducts
from saving.models import SavingProducts

User = get_user_model()



# class AccountSignUpSerializer(RegisterSerializer):

        
    
#     # region = serializers.CharField(max_length=100)
#     # sex = serializers.CharField(max_length=20)
#     birth_date = serializers.DateField()
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from allauth.utils import email_address_exists, get_username_max_length
from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.utils.translation import gettext_lazy as _

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=allauth_account_settings.USERNAME_REQUIRED,
    )
    email = serializers.EmailField(required=allauth_account_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    # 추가
    realname = serializers.CharField(
        required=True,
        max_length=255
    )

    nickname = serializers.CharField(
        required=False,
        allow_blank=True, 
        max_length=50,
    )

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _('A user is already registered with this e-mail address.'),
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            # 추가
            'realname': self.validated_data.get('realname', ''),
        }

    # https://github.com/pennersr/django-allauth/blob/master/allauth/account/adapter.py
    def save(self, request):
        # allauth의 기본 adapter를 가져옴
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        # 기본 adapter의 save_user는 nickname 필드를 저장하지 않는다!
        # save_user: 기본적인 입력 부분만 반환하도록 되어있음
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )
        # adapter를 새로 오버라이딩해서 해결함
        user.realname = self.cleaned_data['realname']   # 추가
        user.save()

        profile = Profile.objects.create(user=user)

        # You can then set the optional fields if needed
        profile.bio = 'Some bio text'
        profile.avatar = 'path/to/avatar.jpg'
        # Set other optional fields as required

        # Save the profile
        profile.save()



        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class AccountSignUpSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ('name', 'identification', 'password', 'email')


class CommentSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Comment
        fields = ['id', 'content', ]  # Add more fields as needed

    

class ArticleSerializer(serializers.ModelSerializer):
    
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'category', 'like_count', 'comment_count']  # Add more fields as needed
    def get_comment_count(self, obj):
        return obj.comments.count()



class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = ['id','fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'like_deposit_count', 'register_deposit_count']  # Add more fields as needed
class SavingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = ['id','fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'like_saving_count', 'registered_saving_count']  # Add more fields as needed


class JJINProfilesSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile
        fields = '__all__'


class JJJINProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'stock_amount', 'bond_amount', 'loan_amount', 'cash_equivalents_amount', 'property_amount']








class ProfileViewSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)
    
    profile = JJINProfilesSerializer()
    articles = ArticleSerializer(many=True, read_only=True)
    like_comments = CommentSerializer(many=True, read_only=True)
    like_articles = ArticleSerializer(many=True, read_only=True)
    like_deposit_list = DepositProductSerializer(many=True, read_only=True)
    registered_deposit_list = DepositProductSerializer(many=True, read_only=True)
    like_saving_list = SavingProductSerializer(many=True, read_only=True)
    registered_saving_list = SavingProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['realname', 'profile', 'username', 'email', 'region', 'sex', 'age', 'income', 'ready_money',  'articles', 'like_comments', 'like_articles', 'like_deposit_list', 'registered_deposit_list', 'like_saving_list', 'registered_saving_list' ]





class ProfileEditSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    articles = ArticleSerializer(many=True, read_only=True)
    like_comments = CommentSerializer(many=True, read_only=True)
    like_articles = ArticleSerializer(many=True, read_only=True)
    like_deposit_list = DepositProductSerializer(many=True, read_only=True)
    registered_deposit_list = DepositProductSerializer(many=True, read_only=True)
    like_saving_list = SavingProductSerializer(many=True, read_only=True)
    registered_saving_list = SavingProductSerializer(many=True, read_only=True)
    
    # Include the additional fields as regular fields, without nested objects
    loan_amount = serializers.DecimalField(max_digits=11, decimal_places=2, required=False)
    stock_amount = serializers.DecimalField(max_digits=11, decimal_places=2, required=False)
    bond_amount = serializers.DecimalField(max_digits=11, decimal_places=2, required=False)
    cash_equivalents_amount = serializers.DecimalField(max_digits=11, decimal_places=2, required=False)
    property_amount = serializers.DecimalField(max_digits=11, decimal_places=2, required=False)
    cash_hyup_count = serializers.IntegerField(default=0)
    cash_content_count = serializers.IntegerField(default=0)
    
    class Meta:
        model = Profile
        fields = [
            'loan_amount', 'stock_amount', 'bond_amount', 'cash_equivalents_amount', 'property_amount',
            'cash_hyup_count', 'cash_content_count',
            'user', 'articles', 'like_comments', 'like_articles',
            'like_deposit_list', 'registered_deposit_list',
            'like_saving_list', 'registered_saving_list',
        ]






# class ProfileSerializer(serializers.ModelSerializer):
#     # comments = CommentSerializer(many=True, read_only=True)
    
#     user = UserSerializer()
#     articles = ArticleSerializer(many=True, read_only=True)
#     like_comments = CommentSerializer(many=True, read_only=True)
#     like_articles = ArticleSerializer(many=True, read_only=True)
#     like_deposit_list = DepositProductSerializer(many=True, read_only=True)
#     registered_deposit_list = DepositProductSerializer(many=True, read_only=True)
#     like_saving_list = SavingProductSerializer(many=True, read_only=True)
#     registered_saving_list = SavingProductSerializer(many=True, read_only=True)
    


#     class Meta:
#         model = Profile
#         fields = ['loan_amount' , 'user',   'articles', 'like_comments', 'like_articles', 'like_deposit_list', 'registered_deposit_list', 'like_saving_list', 'registered_saving_list' ]








class LoginSerializer(RegisterSerializer):

    pass
    