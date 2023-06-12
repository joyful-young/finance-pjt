from django.shortcuts import render
from django.conf import settings
import requests
from finlife.serializers import DepositProductsSerializer, DepositOptionsSerializer, DepositProductsListSerializer, DepositProductSaveSerializer, DepositOptionSaveSerializer
from .models import DepositProducts, DepositOptions
from .forms import DepositProductsForm
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.



# @api_view(["GET"])
# def api_test(request):
#     URL = BASE_URL + 'depositProductSearch.json'



# import requests
# URL = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1"
BASE_URL = "http://finlife.fss.or.kr/finlifeapi/"
api_key = settings.API_KEY

# response = requests.get(URL)
# response.status_code
# response.text





@api_view(["GET"])
@authentication_classes([TokenAuthentication])

def save_deposit_products(request):
    

    depositProducts = f"depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"
    deposit_list_URL = BASE_URL + depositProducts
    
    response = requests.get(deposit_list_URL).json()['result']['baseList']
    response_options = requests.get(deposit_list_URL).json()['result']['optionList']


    for DepositProduct in response:
        if 'kor_co_nm' not in DepositProduct:
            DepositProduct['kor_co_nm'] = -1 

        form = DepositProductSaveSerializer(data=DepositProduct)  
        if form.is_valid(raise_exception=True):
            form.save()
     
    for optionproduct in response_options:
        if not optionproduct["intr_rate"]:
            optionproduct["intr_rate"] = 0

        related_product = DepositProducts.objects.filter(fin_prdt_cd=optionproduct['fin_prdt_cd']).first()
        form = DepositOptionSaveSerializer(data=optionproduct)
        if form.is_valid(raise_exception=True):
            form.save(fin_prdt_cd=related_product)
    
    return JsonResponse({'response':response})

    # response.status_code
    # response.text
   


from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


# GET : 예금 전체 조회 / POST : 예금 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능

def deposit_products(request):
    
    if request.method == "GET": 
        depositProducts = DepositProducts.objects.all()
        user = request.user
        serializer = DepositProductsListSerializer(depositProducts, many=True, context={'user': user})


        return Response(serializer.data)
    else: # 포스트 일 때 상품데이터 저장
        form = DepositProductsSerializer(data=request.POST)  
        if form.is_valid(raise_exception=True):
            form.save()


        else:
            message = {'message': "데이터가 잘못됨"}
            return Response(message)


#상세 예금조회
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능

def detail_deposit_product(request, fin_prdt_cd):
    depositproducts = get_object_or_404(DepositProducts, fin_prdt_cd=fin_prdt_cd)
    
    if request.method == "GET":
        serializer_context = {'user': request.user}
        serializer = DepositProductsSerializer(depositproducts, context = serializer_context)
        data = serializer.data

        try:
            depositproducts.depositProducts_like_deposit.get(id=request.user.id)        
            data['like_flag'] = True
        except:
            data['like_flag'] = False
            
        return Response(data)
    elif request.method == 'PUT':
        serializer = DepositProductsSerializer(depositproducts, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

@api_view(['PUT'])
def update_options(request, id):
    
    depositoptions = get_object_or_404(DepositOptions, id = id)
    
    serializer = DepositOptionsSerializer(depositoptions, data = request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    

    
# @api_view(['GET'])
# @permission_classes([AllowAny]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
# # 상세 조횐데 폐기 
# def deposit_product_options(request, fin_prdt_cd):
#     try:
#         deposit_product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
#         serializer = DepositProductsSerializer(deposit_product)
#         options_serializer = DepositOptionsSerializer(deposit_product.options, many=True)
#         data = {
#             'product': serializer.data,
#             'options': options_serializer.data
#         }
#         return Response(data)
#     except DepositProducts.DoesNotExist:
#         return Response({'message': 'Deposit product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능

def deposit_product_options(request,  fin_prdt_cd):
    id = fin_prdt_cd
    
    deposit_product = DepositProducts.objects.get(fin_prdt_cd = fin_prdt_cd)
    serializer = DepositProductsSerializer(deposit_product)
    
    return Response(serializer.data)
    



@api_view(['POST'])
def like_deposit_product(request, fin_prdt_cd):
    try:
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        user = request.user

        if user in product.like_deposit.all():
            product.like_deposit.remove(user)
            product.like_deposit_count -= 1
            product.save()
            return Response({"message": "예금 상품 좋아요 취소."}, status=status.HTTP_200_OK)
        else:
            product.like_deposit.add(user)
            product.like_deposit_count += 1
            product.save()

            return Response({"message": "예금 상품 좋아요."}, status=status.HTTP_200_OK)
    except DepositProducts.DoesNotExist:
        return Response({"message": "해당 예금 상품이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def register_deposit_product(request, fin_prdt_cd):
    try:
        product = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        user = request.user

        if user in product.register_deposit.all():
            product.register_deposit.remove(user)
            product.register_deposit_count -= 1
            product.save()

            return Response({"message": "예금 상품 가입 취소"}, status=status.HTTP_200_OK)
        else:
            product.register_deposit.add(user)
            product.register_deposit_count += 1
            product.save()


            return Response({"message": "가입한 예금 상품"}, status=status.HTTP_200_OK)
    except DepositProducts.DoesNotExist:
        return Response({"message": "해당 상품이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

# # intr_rate2
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def article_like_list(request):
#     if request.method == 'GET':
#         articles = Article.objects.annotate(like_count_annotation=Count('article_like_user')).order_by('-like_count_annotation')
#         serializer = ArticleListSerializer(articles, many=True)
#         return Response(serializer.data)

from rest_framework.views import APIView
from django.db.models import Max, Min
from .serializers import FirstSerializer
# 최고 금리 순 정렬
@permission_classes([AllowAny])
class max_intr_deposit_products(APIView):
    def get(self, request):
        deposit_products = DepositProducts.objects.all().prefetch_related('options')
        sorted_products = sorted(deposit_products, key=lambda product: product.options.aggregate(max_rate=Max('intr_rate2'))['max_rate'], reverse=True)
        serializer = FirstSerializer(sorted_products, many=True)
        return Response(serializer.data)

@permission_classes([AllowAny])
class kibon_intr_deposit_products(APIView):
    def get(self, request):
        deposit_products = DepositProducts.objects.all().prefetch_related('options')
        sorted_products = sorted(deposit_products, key=lambda product: product.options.aggregate(max_rate=Min('intr_rate'))['max_rate'], reverse=True)
        serializer = FirstSerializer(sorted_products, many=True)
        return Response(serializer.data)





# @api_view(['GET'])
# def top_rate(request):

#     option_products = list(DepositOptions.objects.all())
    
#     option_products.sort(key=lambda x: -x.intr_rate2)

#     top_option = option_products[0]
#     top_product = top_option.fin_prdt_cd
    
#     serailizer = DepositOptionsSerializer(option_products[0])
#     # serializer = DepositOptionsSerializer(option_products, many=True)
    
#     # print(type(serializer.data), '!!!!!')
#     ab = {}
#     return Response(serailizer.data)


#     pass