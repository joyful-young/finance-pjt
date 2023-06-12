from django.db import models
from accounts.models import User

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품 코드
    kor_co_nm = models.TextField()  # 금융 회사명 
    fin_prdt_nm= models.TextField() # 금융 상품명
    etc_note = models.TextField()   # 금융 상품 설명
    join_deny = models.IntegerField() # 가입제한 1, 2, 3 설정해야되는데 -> 일단 안해도 되는거 아닌가?
    join_member = models.TextField()    # 가입 대상
    join_way = models.TextField()   # 가입 방법
    spcl_cnd = models.TextField()   # 우대 조건
    like_deposit = models.ManyToManyField(User, related_name='like_deposit_list', blank=True)
    like_deposit_count = models.PositiveIntegerField(default=0)
    register_deposit = models.ManyToManyField(User, related_name='registered_deposit_list', blank=True)
    register_deposit_count = models.PositiveIntegerField(default=0)


class DepositOptions(models.Model):
    fin_prdt_cd = models.ForeignKey(DepositProducts, on_delete=models.CASCADE ,related_name='options', blank=True)  #외래키    
    intr_rate_type_nm = models.CharField(max_length=300)                                    # 저축 금리 유형명
    intr_rate = models.FloatField()                                                            # 저축금리
    intr_rate2 = models.FloatField()    #최고 우대금리
    save_trm = models.IntegerField() # 저축기간 단위: 개월


    
    @staticmethod
    def send_interest_rate_update_email(deposit_options):
    # Retrieve the registered users for the deposit product
        
        try:
            registered_users = deposit_options.fin_prdt_cd.register_deposit.all()
        except:
            return 

        for user in registered_users:
            subject = 'Interest Rate Update'
            message = f'The interest rate for the deposit product "{deposit_options.fin_prdt_cd.fin_prdt_nm}" has been updated.'
            from_email = 'your_email@example.com'
            to_email = user.email
            print('Loaded here * n')
            send_mail(subject, message, from_email, [to_email])





    def save(self, *args, **kwargs):
        # Check if the instance is being updated
        if self.pk:
            # Get the previous state of the instance
            previous_state = DepositOptions.objects.get(pk=self.pk)

            # Check if the interest rate has been modified
            if previous_state.intr_rate != self.intr_rate or previous_state.intr_rate2 != self.intr_rate2:
                # Call the static method to send the email notification
                self.send_interest_rate_update_email(self)

        super().save(*args, **kwargs)

# Signal receiver to handle post-save event
@receiver(post_save, sender=DepositOptions)
def handle_interest_rate_update(sender, instance, **kwargs):
    # Call the static method to send the email notification
    print('이메일 보냈다')
    instance.send_interest_rate_update_email(sender)