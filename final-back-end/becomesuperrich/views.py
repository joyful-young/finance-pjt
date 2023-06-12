from django.shortcuts import render
from rest_framework.response import Response
from accounts.models import User, Profile
# Create your views here.
from community.models import Article
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from finlife.models import DepositProducts
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.db.models import Count
from rest_framework.renderers import JSONRenderer
import json

# # 코사인 유사도 계산
# def calculate_similarity_for_open(profile1, profile2):
#     # profile1과 profile2가 좋아요를 누른 게시글의 ID 가져오기
#     profile1_article_ids = profile1.like_articles.values_list('id', flat=True)
#     profile2_article_ids = profile2.like_articles.values_list('id', flat=True)

#     # profile1과 profile2가 좋아요를 누른 댓글의 ID 가져오기
#     profile1_comment_ids = profile1.like_comments.values_list('id', flat=True)
#     profile2_comment_ids = profile2.like_comments.values_list('id', flat=True)

#     # profile1과 profile2의 유일한 아이템 ID 세트 생성
#     item_ids = set(profile1_article_ids).union(set(profile2_article_ids)).union(set(profile1_comment_ids)).union(set(profile2_comment_ids))

#     # profile1과 profile2의 아이템 상호작용을 나타내는 벡터 생성
#     profile1_vector = np.array([1 if item_id in profile1_article_ids else 0 for item_id in item_ids])
#     profile2_vector = np.array([1 if item_id in profile2_article_ids else 0 for item_id in item_ids])

#     # 두 벡터 사이의 코사인 유사도 계산
#     similarity = cosine_similarity([profile1_vector], [profile2_vector])[0][0]

#     return similarity
from django.db.models import F

def calculate_similarity_for_open(profile1, profile2):
    # profile1과 profile2가 좋아요를 누른 게시글의 ID 가져오기
    print(len(list(profile1.user.like_articles.all())), '이거')
    profile1_article_ids = profile1.user.like_articles.values_list('id', flat=True)
    profile2_article_ids = profile2.user.like_articles.values_list('id', flat=True)
    
    # profile1과 profile2가 좋아요를 누른 댓글의 ID 가져오기
    profile1_comment_ids = profile1.user.like_comments.values_list('id', flat=True)
    profile2_comment_ids = profile2.user.like_comments.values_list('id', flat=True)

    # profile1과 profile2의 유일한 아이템 ID 세트 생성
    item_ids = set(profile1_article_ids).union(set(profile2_article_ids)).union(set(profile1_comment_ids)).union(set(profile2_comment_ids))

    # profile1과 profile2의 아이템 상호작용을 나타내는 벡터 생성
    profile1_vector = np.array([1 if item_id in profile1_article_ids else 0 for item_id in item_ids])
    profile2_vector = np.array([1 if item_id in profile2_article_ids else 0 for item_id in item_ids])

    #코사인 유사도 계산
    similarity = cosine_similarity([profile1_vector], [profile2_vector])[0][0]

    return similarity





from statistics import mean
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def collaborative_filtering_recommendation(request):
    

    your_stock_amount = request.user.profile.stock_amount
    your_bond_amount = request.user.profile.bond_amount
    your_loan_amount = request.user.profile.loan_amount
    your_cash_equivalents_amount = request.user.profile.cash_equivalents_amount
    # print('request.user', request.user)
    print(your_stock_amount, your_bond_amount, your_loan_amount, your_cash_equivalents_amount)
    
    # 예외 구현
    if  not (your_stock_amount and your_bond_amount and your_loan_amount and your_cash_equivalents_amount):
        return Response({'msg': '모든 포트폴리오를 입력해주시면 추천 알고리즘 제공이 가능합니다.', 'jongryu': 0 })
    

    your_profile = request.user.profile

    if request.user.like_articles.count() <5:
        return Response({'msg': '커뮤니티 활동이 부족합니다. 커뮤니티 활동을 충분히 하시면 맞춤형 추천을 제공해드리겠습니다.',  'jongryu': 1})


    # Get the total count of profiles
    total_profiles = Profile.objects.count()

    # Calculate the number of profiles in the top 10%
    top_10_percent = int(total_profiles * 0.1)

    # Retrieve the profiles in the top 10% based on property_amount
    higher_asset_users = Profile.objects.order_by('-property_amount')[:top_10_percent]
    # higher_asset_users = Profile.objects.all()
    # print(higher_asset_users, '상위 자산 유저')
    # 게시글 좋아요, 댓글 좋아요, 댓글이 달린 게시글을 기반으로 한 협업 필터링 유사도 계산
    similarity_scores = {}
    for user_profile in higher_asset_users:

        # 게시글 좋아요, 댓글 좋아요, 댓글이 달린 게시글을 기반으로 유사도 계산
        similarity = calculate_similarity_for_open(your_profile, user_profile)
        similarity_scores[user_profile.id] = similarity
        print(similarity, '시밀러리티ㅇ')
    # 상위 10개 유사한 사용자 선택
    top_similar_users = sorted(similarity_scores, key=similarity_scores.get, reverse=True)[:10]
    print(top_similar_users, '상위 10개 유저')
    # 유사도 점수를 기반으로 포트폴리오의 가중평균 계산
    weighted_portfolios = []
    for user_id in top_similar_users:
        user_profile = Profile.objects.get(id=user_id)
        similarity = similarity_scores[user_id]
        print(type(user_profile.stock_amount) , '타입')
        weighted_portfolios.append({
            'stock_amount': float(user_profile.stock_amount) * similarity,
            'bond_amount': float(user_profile.bond_amount) * similarity,
            'loan_amount': float(user_profile.loan_amount) * similarity,
            'cash_equivalents_amount': float(user_profile.cash_equivalents_amount) * similarity
        })

    # 나의 포트폴리오 각 항목의 비율 계산
    total_amount = your_stock_amount + your_bond_amount + your_loan_amount + your_cash_equivalents_amount
    your_ratios = {
        'stock_ratio': float(your_stock_amount / total_amount),
        'bond_ratio': float(your_bond_amount / total_amount),
        'loan_ratio': float(your_loan_amount / total_amount),
        'cash_ratio': float(your_cash_equivalents_amount / total_amount)
    }
    weighted_average_portfol = {}
    # 비율을 가중평균 포트폴리오와 비교하여 가장 큰 차이가 나는 항목 찾기
    max_difference = 0
    total_weighted_amount = 0
    print('디버깅', weighted_portfolios)
    max_difference_field = None
    for field in ['stock_amount', 'bond_amount', 'loan_amount', 'cash_equivalents_amount']:
        for portfolio in weighted_portfolios:
            
            try:
                weighted_average_portfol.get(field)
                weighted_average_portfol[field] += portfolio[field] 

            except:
                weighted_average_portfol[field] = portfolio[field] 
    
            total_weighted_amount += weighted_average_portfol[field]
    print('비율', weighted_average_portfol)
    for field in ['stock_amount', 'bond_amount', 'loan_amount', 'cash_equivalents_amount']:
        
            weighted_average_portfol[field] /= total_weighted_amount
    for field in ['stock_amount', 'bond_amount', 'loan_amount', 'cash_equivalents_amount']:
        
        difference = your_ratios[field.split('_')[0] + '_ratio'] - weighted_average_portfol[field]
        if difference > max_difference and difference>0:
            max_difference = difference
            max_difference_field = field
    
        

    # 예적금 추천 함수 시작
    if max_difference_field == 'cash_equivalents_amount':
        
                        
        # 너의 포폴 중 상위권과 가장 차이나는 항목 / 차이나는 정도
        return Response({'difference': max_difference,'field':max_difference_field})
    
    elif max_difference_field == 'loan_amount':
        # 너의 포폴 중 상위권과 가장 차이나는 항목 / 차이나는 정도

        return Response({'difference': max_difference,'field':max_difference_field})

        

    elif max_difference_field == 'bond_amount':
        
        
        return Response({'difference': max_difference,'field':max_difference_field})

        
    elif max_difference_field == 'stock_amount':
        
        
        return Response({'difference': max_difference,'field':max_difference_field})

        

















@api_view(['GET'])
@permission_classes([AllowAny])

def recommend_portfolio(request):
    # 유저 데이터와 전체 유저 데이터를 어떻게 가져올지에 따라 코드를 수정해야합니다.
    # 예시로 user_data와 all_users_data를 하드코딩하여 사용합니다.
    user_data = {
        'loan_amount': 10000,
        'cash_equivalents_amount': 5000,
        'bond_amount': 20000,
        'stock_amount': 30000
    }

    all_users_data = [
        {
            'loan_amount': 5000,
            'cash_equivalents_amount': 10000,
            'bond_amount': 30000,
            'stock_amount': 20000
        },
        {
            'loan_amount': 20000,
            'cash_equivalents_amount': 30000,
            'bond_amount': 5000,
            'stock_amount': 10000
        },
        # 다른 유저 데이터들...
    ]

    user_vector = np.array([user_data['loan_amount'], user_data['cash_equivalents_amount'], user_data['bond_amount'], user_data['stock_amount']])
    user_vector = user_vector.reshape(1, -1)  # 1차원 벡터를 2차원으로 변환

    all_users_vector = np.array([[user['loan_amount'], user['cash_equivalents_amount'], user['bond_amount'], user['stock_amount']] for user in all_users_data])

    similarities = cosine_similarity(user_vector, all_users_vector)

    most_similar_user_index = np.argmax(similarities)
    most_similar_user = all_users_data[most_similar_user_index]
    
    total_amount = most_similar_user['loan_amount'] + most_similar_user['cash_equivalents_amount'] + most_similar_user['bond_amount'] + most_similar_user['stock_amount']

    recommendation = {
        'loan_ratio': most_similar_user['loan_amount'] / total_amount *100,
        'cash_equivalents_ratio': most_similar_user['cash_equivalents_amount'] / total_amount *100,
        'bond_ratio': most_similar_user['bond_amount'] / total_amount *100,
        'stock_ratio': most_similar_user['stock_amount'] / total_amount *100
    }

    return Response(recommendation)


# user_portfolio, recommended_portfolio
# 포트폴리오 점수화
def compare_portfolios(user_portfolio, all_users_data):
    
    recommended_portfolio = recommend_portfolio(user_portfolio, all_users_data)
    
    scores = {}  # 각 항목의 점수를 저장할 딕셔너리

    # 각 항목별로 점수 계산
    for key in user_portfolio.keys():
        user_value = user_portfolio[key]
        recommended_value = recommended_portfolio[key]
        ratio = abs((user_value - recommended_value) / user_value)
        score = 100 - (ratio * 100)
        scores[key] = score

    # 평균 점수 계산
    average_score = sum(scores.values()) / len(scores)

    # 가장 많이 차이나는 항목 찾기
    max_difference_item = max(scores, key=scores.get)
    data = {
        "average_score": average_score,
        "max_difference_item": max_difference_item,
        "recommended_portfolio": recommended_portfolio
    }

    return Response(data)

# 협업과 콘첸트 기반 이름 바꿔야해
# 협업 필터링 방식 예금 추천
from django.db.models import Count

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from finlife.models import DepositProducts
from saving.models import SavingProducts



# 협업 필터링 방식. calculate_similarity(user, other_user) 어떤 함수로 구현할지 생각해봐야함
# 코사인 유사도로 유사도 계산.
@permission_classes([IsAuthenticated])
def calculate_similarity(user, other_user):
    # 사용자와 다른 사용자의 데이터를 벡터로 변환.
    user_vector = np.array([user.stock_amount, user.bond_amount, user.property_amount])
    other_user_vector = np.array([other_user.stock_amount, other_user.bond_amount, other_user.property_amount])

    #  코사인 유사도를 계산.
    similarity_score = np.dot(user_vector, other_user_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(other_user_vector))
    
    return similarity_score
    
# 작동하니까 리스폰스 빼놔 나중에 딕셔너리로 바꿔야해
@permission_classes([AllowAny])
def recommend_unregistered_product(user):
    all_products = list(DepositProducts.objects.all()) + list(SavingProducts.objects.all())

    # 사용자가 등록한 예금 및 적금 상품의 인덱스를 가져옵니다.
    registered_indices = list(user.registered_deposit_list.values_list('id', flat=True)) + list(user.registered_saving_list.values_list('id', flat=True))
    print(1)
    # 사용자와 같은 상품을 등록한 다른 사용자와의 유사도를 계산합니다.
    similarity_scores = []
    unique_users = set()

    for product_id in registered_indices:
        # 같은 예금 상품을 등록한 사용자를 찾습니다.
        users_with_same_deposit = User.objects.filter(registered_deposit_list__id=product_id).exclude(id=user.id)

        # 같은 예금 상품을 등록한 사용자와의 유사도를 계산합니다.
        for other_user in users_with_same_deposit:
            try:
                _ = other_user.profile
                similarity_score = calculate_similarity(user.profile, other_user.profile)
            except:
                continue
            
            if other_user not in unique_users:
                similarity_scores.append((other_user, similarity_score))
                unique_users.add(other_user)

        # 같은 적금 상품을 등록한 사용자를 찾습니다.
        users_with_same_saving = User.objects.filter(registered_saving_list__id=product_id).exclude(id=user.id)

        # 같은 적금 상품을 등록한 사용자와의 유사도를 계산합니다.
        for other_user in users_with_same_saving:
            similarity_score = calculate_similarity(user, other_user)
            if other_user not in unique_users:
                similarity_scores.append((other_user, similarity_score))
                unique_users.add(other_user)

    # 유사도 점수를 기준으로 사용자를 내림차순으로 정렬합니다.
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    print(similarity_scores)
    i = 0
    serialized_product = []
    for other_user, similarity_score in similarity_scores:
        # 다른 사용자가 등록한 상품을 가져옵니다.
        print(other_user.username)
        other_user_registered_products = other_user.registered_deposit_list.exclude(id__in=registered_indices).union(other_user.registered_saving_list.exclude(id__in=registered_indices))
        print(other_user_registered_products)
        # 다른 사용자의 등록되지 않은 상품을 추천 상품에 추가합니다.
        for product in other_user_registered_products:
            flag = False
            for i in serialized_product:
                if product.id == serialized_product[i]['id']:
                    flag = True
                    break
            if flag:
                continue
            # if i == 3:
            #     break

            print(product.fin_prdt_cd, 'cd')

            serialized_product.append( (product.id, product.fin_prdt_nm))


            # serialized_product[i] = {
            # 'id': product.id,
            # 'name': product.fin_prdt_nm,
            # }
            
            i+=1
    print(serialized_product)
    return serialized_product














# 콘텐츠 기반 필터링. 예금 상품들의 설명으로 tfi 유사도를 계싼하고
# 유사도가 가장 높은 상품부터 3개 반환

@permission_classes([AllowAny])
def recommend_content_based(user):
    # 모든 예금 및 적금 상품 데이터 가져오기
    all_products = list(DepositProducts.objects.all()) + list(SavingProducts.objects.all())
    
    # 제품 설명을 기반으로 TF-IDF 벡터화 수행
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([product.etc_note for product in all_products])

    # 사용자가 좋아하는 상품 및 구독한 상품의 인덱스 가져오기
    user_likes = list(user.like_deposit_list.values_list('id', flat=True)) + list(user.like_saving_list.values_list('id', flat=True))
    user_subscriptions = list(user.registered_deposit_list.values_list('id', flat=True)) + list(user.registered_saving_list.values_list('id', flat=True))
    user_preferences = set(user_likes + user_subscriptions)

    # 사용자 기호에 기반하여 유사한 상품 찾기
    similarity_scores = linear_kernel(tfidf_matrix, tfidf_matrix)
    similar_products_indices = similarity_scores.argsort()[0][::-1]

    recommended_products = []
    i = 0
    for index in similar_products_indices:
        product = all_products[index]
        if product.id not in user_preferences and len(recommended_products) < 5:
            
            recommended_products.append(( product.id,
                 product.fin_prdt_nm, product.fin_prdt_cd, product.kor_co_nm)) 
            i += 1

        if len(recommended_products) == 5:
            break
    print(recommended_products)
    return recommended_products



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hybrid_recommendation(request):
    # 협업 필터링을 통한 추천
    user = request.user

    collaborative_recommendation = recommend_unregistered_product(user)

    # 콘텐츠 기반 필터링을 통한 추천
    content_based_recommendation = recommend_content_based(user)

    # 가중치를 설정하여 추천 결과를 조합
    
    collaborative_count = user.profile.cash_hyup_count
    content_based_count = user.profile.cash_content_count
    print(collaborative_count, content_based_count)
    total_count = 0
    if content_based_count and  collaborative_count:
        
        total_count = collaborative_count + content_based_count
    if total_count!=0:
        collaborative_weight = collaborative_count / total_count  
    else:
        collaborative_weight = 0.5
    # if 66% 이상, 몇퍼 이상이면 개수 가변하게. 일단 보류
    if collaborative_weight > 0.65:
        val = 4
    elif collaborative_weight > 0.45:
        val = 3
    elif collaborative_weight > 0.33:
        val = 2
    
    print(collaborative_recommendation)
    print(content_based_recommendation)
    # 최종 추천 결과 계산
    # final_recommendation = collaborative_recommendation * collaborative_weight + content_based_recommendation * content_based_weight
    final_recommendation = collaborative_recommendation[:val]  + content_based_recommendation[:(6-val)] 
    print(len(final_recommendation), '이게 안찍히지?')
    if len(final_recommendation) <6 :
        difference_length = 6-len(final_recommendation)
        top_products = DepositProducts.objects.order_by('-like_deposit_count')[:difference_length]
        product_list = [(product.id, product.fin_prdt_nm, product.fin_prdt_cd, product.kor_co_nm) for product in top_products]
        final_recommendation += product_list
        data = {'final_recommendation': final_recommendation }
    #final_recommendation
    return Response(data)



# Q-Learning Algorithms


# from django.shortcuts import render





# # Q-테이블 및 기타 변수 초기화
# num_actions = 2  # Number of possible actions (collaborative, content-based)
# num_states = 10  # Number of possible states
# Q = np.random.rand(num_states, num_actions)
# alpha = 0.5  # Learning rate
# gamma = 0.9  # Discount factor
# epsilon = 0.1  # Exploration rate

# def hybrid_recommendation(user):
#     # 협업 필터링을 통한 추천
#     collaborative_recommendation = recommend_deposit(user)

#     # 콘텐츠 기반 필터링을 통한 추천
#     content_based_recommendation = recommend_deposit_content_based(user)

#     # greedy 사용하여 액션 선택
#     if np.random.uniform() < epsilon:
#         action = np.random.randint(num_actions)  # Exploration
#     else:
#         state = encode_state(user)  
#         action = np.argmax(Q[state])  # Exploitation

#      # 선택된 액션 수행 및 최종 추천 획득
#     if action == 0:
#         final_recommendation = collaborative_recommendation
#     else:
#         final_recommendation = content_based_recommendation

#      # 받은 보상에 기반하여 Q-테이블 업데이트
#     reward = calculate_reward(final_recommendation)
#     next_state = encode_state(user)  # 액션 수행 후 다음 상태를 인코딩
#     Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])

#     return final_recommendation

# # 상태 인코드
# def encode_state(user):
#     # 우선 나이로 넣어놨음
#     age = user.age
#     if age < 18:
#         state = 0
#     elif age < 30:
#         state = 1
#     elif age < 50:
#         state = 2
#     else:
#         state = 3

#     return state

# def calculate_reward(recommendation):
#     # 사용자 참여도에 기반하여 보상 계산
#     if recommendation.engagement > 0.5:
#         reward = 1.0
#     else:
#         reward = 0.0
#     return reward


# 폐긴데 뭔가 지우기 싫어 ㅠㅠ
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def recommend_unregistered_product(request):
#     all_products = list(DepositProducts.objects.all()) + list(SavingProducts.objects.all())

#     # 사용자가 등록한 예금 및 적금 상품의 인덱스를 가져옵니다.
#     registered_indices = list(request.user.registered_deposit_list.values_list('id', flat=True)) + list(request.user.registered_saving_list.values_list('id', flat=True))
#     print(1)
#     # 사용자와 동일한 상품을 등록한 다른 사용자들 사이의 유사도를 계산.
#     similarity_scores = []
#     for product_id in registered_indices:
#         # 동일한 상품을 등록한 사용자들
#         users_with_same_deposit = User.objects.filter(registered_deposit_list__id=product_id).exclude(id=request.user.id)
#         print(type(list(users_with_same_deposit)))
#         print((list(users_with_same_deposit)))
#         # 동일한 상품을 등록한 사용자들
#         # for other_user in users_with_same_product:
#         #     similarity_score = calculate_similarity(request.user, other_user)
#         #     similarity_scores.append((other_user, similarity_score))

#     # 유사도 점수를 기준으로 사용자들을 내림차순으로 정렬
#     similarity_scores.sort(key=lambda x: x[1], reverse=True)

#     recommended_products = []
#     for other_user, similarity_score in similarity_scores:
#         # 다른 사용자가 등록한 상품들을 가져옵니다.
#         other_user_registered_products = other_user.registered_deposit_list.filter(id__in=registered_indices).union(other_user.registered_saving_list.filter(id__in=registered_indices))

#         # 다른 사용자의 등록되지 않은 상품을 추천 상품에 추가합니다.
#         for product in other_user_registered_products:
#             if product.id not in registered_indices and len(recommended_products) < 3:
#                 recommended_products.append(product)

#         if len(recommended_products) == 3:
#             break

#     return Response(recommended_products)
# # 학습 루프 (Q-학습 알고리즘을 훈련하기 위해 이 루프를 실행)
# num_episodes = 1000  # 에피소드 수
# for episode in range(num_episodes):
#     # 환경 초기화 및 사용자 초기화
#     user = reset_environment()

#     # 한 에피소드를 실행
#     while not episode_finished:
#         recommendation = hybrid_recommendation(user)
#         reward = calculate_reward(recommendation)
#         next_state = encode_state(user)
#         Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
#         state = next_state

# def your_view(request):
#     # 요청 또는 세션에서 사용자 정보 가져오기
#     user = request.user  # 가정: Django의 내장 User 모델을 사용 중
#     # 혼합 추천 함수 호출하여 추천 획득
#     recommendation = hybrid_recommendation(user)

#     # 받은 보상에 기반하여 Q-테이블 업데이트
#     state = encode_state(user)
#     action = 0  # 협업 추천이 인덱스 0인 액션으로 가정
#     reward = calculate_reward(recommendation)
#     next_state = encode_state(user)
#     Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])

#     # 추천과 함께 템플릿 렌더링
#     response_data = {
#         'recommendation': recommendation,
#     }
#     return Response(response_data)