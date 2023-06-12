from django.shortcuts import render
from django.conf import settings
import requests
from .serializers import SavingProductsSerializer, SavingOptionsSerializer, SavingProductsListSerializer, SavingSaveProductsSerializer, SavingSaveOptionsSerializer
from .models import SavingProducts, SavingOptions
from django.http import JsonResponse
from rest_framework.decorators  import api_view , permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *
from rest_framework import status

# Create your views here.



BASE_URL = "http://finlife.fss.or.kr/finlifeapi/"
api_key = settings.API_KEY



@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def save_saving_products(request):
    

    savingProducts = f"savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1"
    saving_list_URL = BASE_URL + savingProducts
    
    response = requests.get(saving_list_URL).json()['result']['baseList']
    response_options = requests.get(saving_list_URL).json()['result']['optionList']


    for SavingProduct in response:
        if 'kor_co_nm' not in SavingProduct:
            SavingProduct['kor_co_nm'] = -1 

        form = SavingSaveProductsSerializer(data=SavingProduct)  
        if form.is_valid(raise_exception=True):
            form.save()
     
    for optionproduct in response_options:
        if not optionproduct["intr_rate"]:
            optionproduct["intr_rate"] = 0

        if not optionproduct["intr_rate2"]:
            optionproduct["intr_rate2"] = 0


        related_product = SavingProducts.objects.filter(fin_prdt_cd=optionproduct['fin_prdt_cd']).first()
        print(SavingProducts.objects.filter(fin_prdt_cd=optionproduct['fin_prdt_cd']).first())
        form = SavingSaveOptionsSerializer(data=optionproduct)
        if form.is_valid(raise_exception=True ):
            form.save(fin_prdt_cd=related_product)
    return JsonResponse({'response':response})



from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


# GET : 적금 조회 / POST : 적금 게시글 작성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능

def saving_products(request):
    
    if request.method == "GET":
        depositProducts = SavingProducts.objects.all()
        user = request.user
        serializer = SavingProductsListSerializer(depositProducts, many=True, context={'user':user})
    
        return Response(serializer.data)
    else: # 포스트 일 때 상품데이터 저장
        form = SavingProductsSerializer(data=request.POST)  
        if form.is_valid(raise_exception=True):
            form.save()
        else:
            message = {'message': "데이터가 잘못됨"}
            return Response(message)
        

# 적금 상세조회
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def saving_product_options(request,  fin_prdt_cd):
    id = fin_prdt_cd
    
    deposit_product = SavingProducts.objects.get(fin_prdt_cd = fin_prdt_cd)
    serializer = SavingProductsSerializer(deposit_product)
    
    return Response(serializer.data)
    

@api_view(['POST'])
def like_saving_product(request, fin_prdt_cd):
    try:
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        user = request.user

        if user in product.like_saving.all():
            product.like_saving.remove(user)
            product.like_saving_count -= 1
            product.save()
            return Response({"message": "예금 상품 좋아요 취소."}, status=status.HTTP_200_OK)
        else:
            product.like_saving.add(user)
            product.like_saving_count += 1
            product.save()

            return Response({"message": "예금 상품 좋아요."}, status=status.HTTP_200_OK)
    except SavingProducts.DoesNotExist:
        return Response({"message": "해당 예금 상품이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def register_saving_product(request, fin_prdt_cd):
    try:
        product = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        user = request.user

        if user in product.registered_saving.all():
            product.registered_saving.remove(user)
            product.registered_saving_count -= 1
            product.save()

            return Response({"message": "예금 상품 가입 취소"}, status=status.HTTP_200_OK)
        else:
            product.registered_saving.add(user)
            product.registered_saving_count += 1
            product.save()


            return Response({"message": "가입한 예금 상품"}, status=status.HTTP_200_OK)
    except SavingProducts.DoesNotExist:
        return Response({"message": "해당 상품이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)










from rest_framework.views import APIView
from django.db.models import Max, Min
from .serializers import FirstSavingSerializer
# 최고 금리 순 정렬
@permission_classes([AllowAny])
class max_intr_saving_products(APIView):
    def get(self, request):
        deposit_products = SavingProducts.objects.all().prefetch_related('saving_options')
        sorted_products = sorted(deposit_products, key=lambda product: product.saving_options.aggregate(max_rate=Max('intr_rate2'))['max_rate'], reverse=True)
        serializer = FirstSavingSerializer(sorted_products, many=True)
        return Response(serializer.data)

@permission_classes([AllowAny])
class kibon_intr_saving_products(APIView):
    def get(self, request):
        deposit_products = SavingProducts.objects.all().prefetch_related('saving_options')
        sorted_products = sorted(deposit_products, key=lambda product: product.saving_options.aggregate(max_rate=Min('intr_rate'))['max_rate'], reverse=True)
        serializer = FirstSavingSerializer(sorted_products, many=True)
        return Response(serializer.data)