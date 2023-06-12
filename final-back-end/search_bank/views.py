from django.shortcuts import render

# Create your views here.
import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import *

@api_view(['POST'])
# @permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 모든 요청 가능, 인증되지 않은 사용자는 GET만 가능
@permission_classes([IsAuthenticated])

def search_nearby_banks(request):
    print('들어오지조차않는걸까')
    location = request.data.get('location')
    bank = request.data.get('bank')

    # Perform API request to Kakao Maps API
    headers = {'Authorization': f'KakaoAK {settings.KAKAO_MAPS_API_KEY}'}
    print(headers)
    params = {
        'query': f'{bank} {location}',
        'size': 10
    }
    response = requests.get('https://dapi.kakao.com/v2/local/search/keyword.json', headers=headers, params=params)
    data = response.json()
    # Extract bank information from the response
    banks = []
    if data:
        for place in data['documents']:
            bank_info = {
                'name': place['place_name'],
                'address': place['address_name'],
                'latitude': place['y'],
                'longitude': place['x']
            }
            banks.append(bank_info)
    
    return Response(banks)