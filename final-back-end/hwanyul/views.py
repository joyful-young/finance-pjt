from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import *


# Create your views here.
import requests
from django.http import JsonResponse
from django.conf import settings
# @permission_classes([AllowAny])

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
def convert_currency(request):
    country = request.GET.get('country')
    amount = request.GET.get('amount')
    conversionType = request.GET.get('conversionType')
    print(conversionType)
    hwanyul_key = settings.HWANYUL_KEY
    response = requests.get(f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={hwanyul_key}&searchdate=20180102&data=AP01')
  

    # 우선 0번에서 전신환(송금) 으로 해놨음
    all_li = response.json()
    hwanyul = 0
    for item in all_li:
        if item['cur_unit'] == country:
            hwanyul = item['deal_bas_r']
            hwanyul = hwanyul.replace(',', '')
            break
        
            # 어마운트가 있으면
    if conversionType == 'krw-to-foreign':
        converted_amount = int(amount) * float(hwanyul)
        print(converted_amount)
    else:
        converted_amount = int(amount)/float(hwanyul)
        # print('{', end='')
        # print(f"name: \"{item['cur_nm']}\", code: \"{item['cur_unit']}\"" , end='')
        # print('}', ',')
        
    return JsonResponse({'converted_amount': converted_amount})