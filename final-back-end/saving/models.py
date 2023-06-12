from django.db import models
from accounts.models import User


# Create your models here.


class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    kor_co_nm = models.TextField()  # 금융 회사명 
    fin_prdt_nm= models.TextField() # 금융 상품명
    etc_note = models.TextField()   # 금융 상품 설명
    join_deny = models.IntegerField() # 가입제한 1, 2, 3 설정해야되는데 -> 일단 안해도 되는거 아닌가?
    join_member = models.TextField()    # 가입 대상
    join_way = models.TextField()   # 가입 방법
    spcl_cnd = models.TextField()   # 우대 조건
    like_saving = models.ManyToManyField(User, related_name='like_saving_list', blank=True)
    like_saving_count = models.PositiveIntegerField(default=0)
    registered_saving = models.ManyToManyField(User, related_name='registered_saving_list', blank=True)
    registered_saving_count = models.PositiveIntegerField(default=0)

class SavingOptions(models.Model):
    fin_prdt_cd = models.ForeignKey(SavingProducts, on_delete=models.CASCADE , related_name='saving_options', blank=True)  #외래키    
    intr_rate_type_nm = models.CharField(max_length=300)                                    # 저축 금리 유형명
    intr_rate = models.FloatField()                                                            # 저축금리
    intr_rate2 = models.FloatField()    #최고 우대금리
    save_trm = models.IntegerField() # 저축기간 단위: 개월