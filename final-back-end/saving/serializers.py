from rest_framework import serializers
from .models import SavingProducts, SavingOptions



class SavingOptionsSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)
class SavingProductsSerializer(serializers.ModelSerializer):
    saving_options = SavingOptionsSerializer(many=True, read_only=True)
  
    class Meta:
        model = SavingProducts
        fields = '__all__'



# 좋아요 수랑 가입자 수 포함된 리스트 시리얼라이저
class SavingProductsListSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)
    liked_by_user = serializers.SerializerMethodField()
    registerd_by_user  = serializers.SerializerMethodField()
    
    def get_liked_by_user(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            return user in obj.like_saving.all()
        return False
    
    def get_registerd_by_user(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            return user in obj.registered_saving.all()
        return False

    class Meta:
        model = SavingProducts
        fields = '__all__' 






class FirstSavingSerializer(serializers.ModelSerializer):
    saving_options = SavingOptionsSerializer(many=True, read_only=True)
    highest_intr_rate2 = serializers.SerializerMethodField()
    min_intr_rate = serializers.SerializerMethodField() 
    class Meta:
        model = SavingProducts
        fields = ('fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'etc_note', 'join_deny',
                  'join_member', 'join_way', 'spcl_cnd', 'like_saving', 'like_saving_count',
                  'registered_saving', 'registered_saving_count', 'saving_options', 'highest_intr_rate2', 'min_intr_rate')

    def get_highest_intr_rate2(self, obj):
        options = obj.saving_options.all()
        if options:
            highest_rate2 = max(options, key=lambda option: option.intr_rate2)
            return highest_rate2.intr_rate2
        return None
    
    def get_min_intr_rate(self, obj):
        options = obj.saving_options.all()  
        if options:
            min_rate = min(options, key=lambda option: option.intr_rate)
            return min_rate.intr_rate
        return None
    

class SavingSaveProductsSerializer(serializers.ModelSerializer):



    class Meta:

        model = SavingProducts
        fields = '__all__' 
        read_only_fields = ('like_saving', 'like_saving_count', 'registered_saving', 'registered_saving_count' )


class SavingSaveOptionsSerializer(serializers.ModelSerializer):


    class Meta:

        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('fin_prdt_cd',)
