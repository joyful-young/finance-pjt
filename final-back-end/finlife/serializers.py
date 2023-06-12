from rest_framework import serializers
from .models import DepositProducts, DepositOptions

class DepositOptionsSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd', 'intr_rate_type_nm', 'intr_rate2', 'save_trm', )


class DepositProductsSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    
    liked_by_user = serializers.SerializerMethodField()
    registered_by_user  = serializers.SerializerMethodField()
    
    def get_liked_by_user(self, obj):
        user = self.context.get('user')
       
        if user and user.is_authenticated:
            return user in obj.like_deposit.all()
        return False
    
    def get_registered_by_user(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            return user in obj.register_deposit.all()
        return False

    class Meta:
        model = DepositProducts
        fields = '__all__'
        # read_only_fields = ('fin_prdt_cd','kor_co_nm', 'fin_prdt_nm', 'etc_note', 'join_deny', 'join_member', 'join_way',)
        


# 좋아요 수랑 가입자 수 포함된 리스트 시리얼라이저
class DepositProductsListSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    liked_by_user = serializers.SerializerMethodField()
    registerd_by_user  = serializers.SerializerMethodField()
    
    def get_liked_by_user(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            return user in obj.like_deposit.all()
        return False
    
    def get_registerd_by_user(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            return user in obj.register_deposit.all()
        return False

    class Meta:
        model = DepositProducts
        fields = '__all__' 


# 최고 순으로 정렬한 시리얼라이저
class FirstSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True)
    highest_intr_rate2 = serializers.SerializerMethodField()
    min_intr_rate = serializers.SerializerMethodField() 
    class Meta:
        model = DepositProducts
        fields = ('fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'etc_note', 'join_deny',
                  'join_member', 'join_way', 'spcl_cnd', 'like_deposit', 'like_deposit_count',
                  'register_deposit', 'register_deposit_count', 'options', 'highest_intr_rate2', 'min_intr_rate')

    def get_highest_intr_rate2(self, obj):
        options = obj.options.all()
        if options:
            highest_rate2 = max(options, key=lambda option: option.intr_rate2)
            return highest_rate2.intr_rate2
        return None
    
    def get_min_intr_rate(self, obj):
        options = obj.options.all()
        if options:
            min_rate = min(options, key=lambda option: option.intr_rate)
            return min_rate.intr_rate
        return None
    



class DepositProductSaveSerializer(serializers.ModelSerializer):


    class Meta:
        model = DepositProducts
        fields = '__all__'
        read_only_fields = ('like_deposit','like_deposit_count', 'register_deposit', 'register_deposit_count', )


class DepositOptionSaveSerializer(serializers.ModelSerializer):


    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)