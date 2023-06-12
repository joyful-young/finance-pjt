from django.urls import path, include
from . import views
# from accounts.views import CustomLoginView, LogoutView
from django.urls import path
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.serializers import SocialLoginSerializer

# 소셜 로그인
BASE_URL = 'http://localhost:8000/accounts/rest-auth/'
KAKAO_CALLBACK_URI = BASE_URL + 'kakao/callback/'
NAVER_CALLBACK_URI = BASE_URL + 'naver/callback/'
GOOGLE_CALLBACK_URI = BASE_URL + 'google/callback/'
GITHUB_CALLBACK_URI = BASE_URL + 'github/callback/'


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callbakc_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer


class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    callback_url = NAVER_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer





app_name = 'accounts'
urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    path('signup/', views.signup),
    # path('login/', CustomLoginView.as_view(), name='rest_login'),
    # path('after_login/', views.after_login, name='after_login'),
    # path('logout/', LogoutView.as_view()  , name='logout'),
    # path('signup/', views.signup, name='signup'),
    path('delete/', views.delete, name='delete'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    
    # 구글 로그인. 되나?
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/', include('allauth.urls')),
    # path('rest-auth/google/login', GoogleLogin.as_view(), name='google'),
    # path('rest-auth/google/callback/', google_callback, name='google_callback'),
    # path('api/v1/accounts/rest-auth/google/login/', GoogleLogin.as_view(), name='google_login'),
    
    # 프로필 수정
    path('edit_profile/<str:username>/', views.edit_profile, name="edit_profile"),

    # 프로필 조회
    path('profile_view/<str:username>/', views.profile_view, name="profile_view"),
    
    # 프로필 공개 여부 설정
    path('set_profile_visibility/', views.set_profile_visibility, name="set_profile_visibility"),
    
    # 프로필 차트
    path('chart-data/<str:username>/', views.DepositChartView.as_view(), name='chartdataview'),
    # 회원가입 체크
    path('unique_check/<str:username>/', views.unique_check, name="unique_check"),
    
    # 개인 메타데이터 생성용 접근 수 체크
    path('increase_count', views.increase_count, name="increase_count"),




    path('create_dummy/<str:username>/', views.create_dummy, name="create_dummy"),




    # path('update/', views.update, name="update"),
    # path('password/', views.change_password, name='change_password'),
    
]

