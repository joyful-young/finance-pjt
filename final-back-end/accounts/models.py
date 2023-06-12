from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class User(AbstractUser):
    # 이름, 아이디(중복확인), 비밀번호, 이메일 만 필수로
    # 옵션 정보 : 지역, 성별, 나이, 가입상품  , 소득 , 보유현금  개인정보에서 알아서 수정 
    GENDER_CHOICES = [
        ('남성', 'Male'),
        ('여성', 'Female'),
    ]
    REGION_CHOICES = [
        ('서울', 'Seoul'),
        ('경기', 'Gyeonggi'),
        ('인천', 'Incheon'),
        ('부산', 'Busan'),
        
    ]

    username = models.CharField( max_length= 30, default='', unique=True )
    realname = models.CharField( max_length= 10, default=''  )
    password = models.CharField(max_length = 30, default='')
    email = models.EmailField(max_length = 40, default='')

    region = models.CharField(max_length=40, choices=REGION_CHOICES, default='')
    sex = models.CharField(max_length=20,  choices=GENDER_CHOICES, null=True, blank=True)
    age = models.IntegerField( null=True, blank=True ) 


    follower = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    income = models.IntegerField( null=True, blank=True )
    ready_money= models.IntegerField( null=True, blank=True )
        
    first_name = None
    last_name = None



    # 공개 여부인데 migrate 하기 싫어서 잠깐 비공개
    profile_public = models.BooleanField( default=True )
    
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)


    # registered_saving_list = models.ForeignKey( SavingProducts, on_delete=models.CASCAED, related_
    # # 프로필 사진
    # profile =  models.CharField(max_length=200, null=True, blank=True)
    # birth_date = models.DateField(null=True, blank=True)
    
    #  팔로워(from_user_id가 팔로우 당한사람 : user_pk)(followings가 팔로우를 한 사람) 목록
    # to_user_id가 팔로우를 신청하면 from_user_id가 팔로우를 당함
    
    # 즉, to_user_id가 팔로우 신청을 하면
    # to_user_id의 followers(=팔로잉 목록) 목록에 from_user_id가 추가 됨
    
    # from_user_id의 followings(=팔로워 목록)에 to_user_id가 추가 됨

    # followings = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    # 싫어하는 장르
    # hate_genres = models.ManyToManyField(Genre, related_name='hate_users', blank=True)



# pillow 깔기
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')
    
    
    # 주식
    stock_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_access_count = models.IntegerField(default=0)
    
    # 채권
    bond_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bond_access_count = models.IntegerField(default=0)
    
    
    # 대출
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loan_access_count = models.IntegerField(default=0)
    
    # 현금성 자산
    cash_equivalents_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cash_equivalents_access_count = models.IntegerField(default=0)

    property_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    @property
    def property1_amount(self):
        fields = [
            self.stock_amount,
            self.bond_amount,
            self.loan_amount,
            self.cash_equivalents_amount
        ]
        if None in fields:
            return None

        return sum(filter(lambda x: x is not None, fields))

    def save(self, *args, **kwargs):
        self.property_amount = self.property1_amount
        super().save(*args, **kwargs)
    
    
    # 현금성 자산 추천 알고리즘에서 사용되는 변수
    cash_hyup_count = models.IntegerField(default=0)
    cash_content_count = models.IntegerField(default=0)


    # ... other fields specific to the profile

    def __str__(self):
        return self.user.username
    
    # @receiver(post_save, sender=User)
    # def create_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_profile(sender, instance, **kwargs):
    #     instance.profile.save()