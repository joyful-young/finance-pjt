from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST, require_safe, require_http_methods
from .forms import CustomUserCreationForm, CustomUserChangeForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import *
from rest_framework.authtoken.models import Token

from dj_rest_auth.views import LoginView

from .serializers import AccountSignUpSerializer, RegisterSerializer, JJJINProfileSerializer, ProfileViewSerializer
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .permissions import IsOwnerOrReadOnly
User = get_user_model()



from django.contrib.auth import get_user_model
from accounts.models import Profile

@api_view(['POST'])
@permission_classes([AllowAny])
def create_dummy(request, username):

    User = get_user_model()

    try:
        # Get the user instance with the specified username
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"User with username '{username}' does not exist.")
        return Response({'msg': 'nokay'})

    # Check if the user has a profile instance
    profile, created = Profile.objects.get_or_create(user=user)

    if not created:
        # Profile instance already exists, update the fields
        profile.bio = 'Updated bio'
        profile.avatar = 'avatars/updated-avatar.png'
        profile.stock_amount = 1000
        profile.stock_access_count = 10
        profile.bond_amount = 2000
        profile.bond_access_count = 20
        profile.loan_amount = 3000
        profile.loan_access_count = 30
        profile.cash_equivalents_amount = 4000
        profile.cash_equivalents_access_count = 40
        profile.property_amount = 5000
        profile.cash_hyup_count = 50
        profile.cash_content_count = 5

        # Save the updated profile
        profile.save()

    return Response({'msg': 'okay'})





@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save(request=request)
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'key': token.key,
            'user' : user.username,
                    }
        return Response(data, status=status.HTTP_201_CREATED)
    

@authentication_classes([TokenAuthentication])
def after_login(request):

    data = {
        'user': request.user
    }

    return Response(data,status=status.HTTP_200_OK)


# @permission_classes([AllowAny])
# class CustomLoginView(LoginView):
#     def get_response(self):
#         response = super().get_response()
#         if self.user is not None:
#             username = self.user.username
#             token_key = response.data['key']
#             response.data['username'] = username
#             response.data['token_key'] = token_key
#         return response

# # 커스텀 로그아웃 토큰으로 작동하는 버전 
# from rest_framework.views import APIView

# @authentication_classes([TokenAuthentication])
# class LogoutView(APIView):
#     """
#     Calls Django logout method and deletes the Token object
#     assigned to the current User object.

#     Accepts/Returns nothing.
#     """
#     def post(self, request, *args, **kwargs):
#         # Get the token associated with the user
#         token = Token.objects.get(user=request.user)

#         # Delete the token
#         token.delete()

#         # Perform logout if necessary (optional)
#         # django_logout(request)

#         # Return the response
#         return Response({'detail': 'Successfully logged out.'})






# 유저 팔로우하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    try:
        user_to_follow = User.objects.get(username=username)
        user = request.user
        if user == user_to_follow:
        
            return Response({"message": "자기 자신을 follow 할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        if user_to_follow in user.following.all():
            user.following.remove(user_to_follow)
            user_to_follow.follower_count -= 1
            user.following_count -= 1
            is_following = False
            user_to_follow.save()
            user.save()
            return Response({"message": "언팔로우 했습니다.", "is_following":is_following}, status=status.HTTP_200_OK)
        else:
            user.following.add(user_to_follow)
            user_to_follow.follower_count += 1
            user.following_count += 1
            is_following = True
            user_to_follow.save()
            user.save()
            
            return Response({"message": "팔로우 했습니다.", "is_following": is_following}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "유저가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

# 프로필 보여주기
@api_view(['GET'])
# @permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def profile_view(request, username):
# 팔로워 수 팔로잉 수 추가하기.
    try:
        user = User.objects.get(username=username )
    except User.DoesNotExist:
        return Response({"message": "유저가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
    # print('1')
    follower_count = user.follower.count()
    following_count = user.following.count()

    serializer = ProfileViewSerializer(user)
    print('2')

    profile_data = serializer.data
    profile_data['follower_count'] = follower_count
    profile_data['following_count'] = following_count

    is_following = user.follower.filter(id=request.user.id).exists()
    profile_data['is_following'] = is_following


    return Response(profile_data) 

from .serializers import ProfileEditSerializer
# 프로필 수정 당장 공부 덜 됨
@api_view(['PUT'])
@permission_classes([IsOwnerOrReadOnly])
def edit_profile(request, username):
    user = request.user
    profile = user.profile
    print(user, profile)
    serializer = ProfileEditSerializer(profile, data=request.data, partial=True)
    print(serializer)
    if serializer.is_valid():
        print('들어오나?')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup(request):
#     serializer = AccountSignUpSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# def logout(request):
#     auth_logout(request)
#     return redirect('articles:index')


# 회원 탈퇴   
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete(request):
    request.user.delete()
    data = {
        'content' : f'{request.user}님의 탈퇴가 완료되었습니다.'
    }
    return Response(data, status=status.HTTP_204_NO_CONTENT)


# 회원 가입 시 중복 확인
@api_view(['GET'])
@permission_classes([AllowAny])
def unique_check(request, username):
    
    try:
        user = User.objects.get(username=username)
        data = {
            'msg': 'NO'
        }
        return Response(data)
    except User.DoesNotExist:
        data = {
            'msg': 'YES'
        }
        return Response(data)

# 프로필 공개여부 설정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def set_profile_visibility(request):
    profile_public = request.data.get('profile_public')
    if profile_public is not None:
        user = request.user
        user.profile_public = profile_public
        user.save()
        serializer = ProfileSerializer(user)
        return Response(serializer.data)
    return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

# 프로필 차트 스켈레톤


from finlife.models import DepositProducts, DepositOptions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

from django.db.models import Max, Min
# 우대 금리 중 
@permission_classes([IsAuthenticated])
class DepositChartView(APIView):
    def get(self, request, username, **kwargs):
        deposit_data = DepositProducts.objects.filter(register_deposit__username=username).values(
            'fin_prdt_nm'
        ).annotate(
            max_intr_rate=Max('options__intr_rate2'),
            kibon_intr_rate=Min('options__intr_rate')
        )

        labels = []
        data = []
        data2 = []
        for item in deposit_data:
            labels.append(item['fin_prdt_nm'])
            data.append(item['max_intr_rate'])
            data2.append(item['kibon_intr_rate'])

        chart_data = {
            'labels': labels,
            'data': data,
            'data2': data2
            
        }

        return Response(chart_data)

from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Profile
@api_view(['POST'])
def increase_count(request):
    if request.method == 'POST':
        header = request.headers.get('X-Header')

        if header == 'stocks':
            profile = get_object_or_404(Profile, user=request.user)
            profile.stock_access_count += 1
            profile.save()
        elif header == 'bond':
            profile = get_object_or_404(Profile, user=request.user)
            profile.bond_access_count += 1
            profile.save()
        elif header == 'saving' or header == 'deposit':
            profile = get_object_or_404(Profile, user=request.user)
            profile.cash_equivalents_access_count += 1
            profile.save()
        elif header == 'loans':
            profile = get_object_or_404(Profile, user=request.user)
            profile.loan_access_count += 1
            profile.save()

        return Response({'msg': 'okay'})
    else:
        return Response({'msg': 'nokay'})





# def update(request):
#     if request.method == 'POST':
#         form = CustomUserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('articles:index') 
#     else:
#         form = CustomUserChangeForm(instance=request.user)
#     context = {'form': form}
#     return render(request, 'accounts/update.html', context)


# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             return redirect('articles:index') 
#     else:
#         form = PasswordChangeForm(request.user)
#     context = {'form': form}
#     return render(request, 'accounts/change_password.html', context)
