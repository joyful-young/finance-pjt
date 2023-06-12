


# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from faker import Faker
# import random
# from accounts.models import User, Profile
# from community.models import Article, Comment
# from finlife.models import DepositProducts

# class Command(BaseCommand):
#     help = 'Creates dummy data for the User model.'

#     def handle(self, *args, **options):
#         # Set the seed for reproducibility
#         random.seed(1234)

#         # Create an instance of the Faker class
#         faker = Faker()

#         # Generate and save dummy data for users and profiles
#         for _ in range(1000):
#             username = faker.user_name()
#             password = faker.password()
#             email = faker.email()
#             user = User.objects.create_user(
#                 username=username,
#                 password=password,
#                 email=email,
#             )
#             profile = Profile.objects.create(
#                 user=user,
#                 bio=faker.paragraph(),
#                 avatar='avatars/default-avatar.png',  # Replace with the actual avatar path
#                 stock_amount=random.uniform(1000, 10000),
#                 bond_amount=random.uniform(1000, 10000),
#                 loan_amount=random.uniform(1000, 10000),
#                 cash_equivalents_amount=random.uniform(1000, 10000),
#                 property_amount=random.uniform(1000, 10000),
#             )

#             self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))

#             # Randomly like and register for deposit products
#             deposit_products = DepositProducts.objects.all()
#             liked_products = random.sample(list(deposit_products), k=random.randint(1, 5))
#             user.like_deposit_list.set(liked_products)

#             registered_products = random.sample(list(deposit_products), k=random.randint(1, 5))
#             user.registered_deposit_list.set(registered_products)

#         # Generate and save dummy data for articles and comments
#         users = User.objects.all()
#         for user in users:
#             for _ in range(random.randint(1, 5)):
#                 article = Article.objects.create(
#                     title=faker.sentence(),
#                     content=faker.paragraph(),
#                     category=faker.word(),
#                     write_user=user,
#                 )
#                 for _ in range(random.randint(0, 3)):
#                     Comment.objects.create(
#                         content=faker.paragraph(),
#                         article=article,
#                         user=user
#                     )

#         self.stdout.write(self.style.SUCCESS('Dummy data generation completed.'))

## 2아래가 2차

# import random
# from django_seed import Seed
# from django.contrib.auth.hashers import make_password
# from accounts.models import User, Profile
# from community.models import Article, Comment
# from finlife.models import DepositProducts, DepositOptions
# from saving.models import SavingProducts, SavingOptions
# seeder = Seed.seeder()

# # Set the random seed for reproducibility
# seeder.random_seed = 42

# # Generate users
# seeder.add_entity(
#     User,
#     100,
#     {
#         'password': make_password('qwer1234!'),
#         'email': lambda x: f'user{x}@example.com',
#         'realname': lambda x: f'User {x}',
#         'region': lambda x: random.choice(['Seoul', 'Gyeonggi', 'Incheon', 'Busan']),
#         'sex': lambda x: random.choice(['Male', 'Female']),
#         'age': lambda x: random.randint(20, 60),
#         'income': lambda x: random.randint(1000, 5000),
#         'ready_money': lambda x: random.randint(1000, 5000),
#     }
# )

# # Generate profiles
# seeder.add_entity(
#     Profile,
#     100,
#     {
#         'bio': lambda x: f'User {x} bio',
#         'avatar': 'avatars/default.png',
#         'stock_amount': lambda x: random.uniform(1000, 10000),
#         'stock_access_count': lambda x: random.randint(0, 10),
#         'bond_amount': lambda x: random.uniform(1000, 10000),
#         'bond_access_count': lambda x: random.randint(0, 10),
#         'loan_amount': lambda x: random.uniform(1000, 10000),
#         'loan_access_count': lambda x: random.randint(0, 10),
#         'property_amount': lambda x: random.uniform(1000, 10000),
        
#         'cash_equivalents_amount': lambda x: random.uniform(1000, 10000),
#         'cash_equivalents_access_count': lambda x: random.randint(0, 10),
#         'cash_hyup_count': lambda x: random.randint(0, 10),
#         'cash_content_count': lambda x: random.randint(0, 10),
#     }
# )

# # Generate articles
# seeder.add_entity(
#     Article,
#     100,
#     {
#         'title': lambda x: f'Article {x}',
#         'content': lambda x: f'Content of Article {x}',
#         'category': lambda x: random.choice(['Category A', 'Category B', 'Category C']),
#         'annoymous_is_active': lambda x: random.choice([True, False]),
#         'write_user': lambda x: User.objects.get(pk=x),
#         'like_count': lambda x: random.randint(0, 100),
#     }
# )

# # Generate comments
# seeder.add_entity(
#     Comment,
#     100,
#     {
#         'content': lambda x: f'Comment {x}',
#         'user': lambda x: User.objects.get(pk=x),
#         'article': lambda x: Article.objects.get(pk=x+1),
#         'like_count': lambda x: random.randint(0, 100),
#     }
# )

# # Generate deposit products
# seeder.add_entity(
#     DepositProducts,
#     10,
#     {
#         'fin_prdt_cd': lambda x: f'DP{x+1}',
#         'kor_co_nm': lambda x: f'Financial Company {x+1}',
#         'fin_prdt_nm': lambda x: f'Deposit Product {x+1}',
#         'etc_note': lambda x: f'Description of Deposit Product {x+1}',
#         'join_deny': lambda x: random.randint(1, 3),
#         'join_member': lambda x: f'Join Member {x+1}',
#         'join_way': lambda x: f'Join Way {x+1}',
#         'spcl_cnd': lambda x: f'Special Condition {x+1}',
#     }
# )

# # Generate deposit options
# seeder.add_entity(
#     DepositOptions,
#     30,
#     {
#         'fin_prdt_cd': lambda x: DepositProducts.objects.get(pk=(x % 10) + 1),
#         'intr_rate_type_nm': lambda x: f'Interest Rate Type {x+1}',
#         'intr_rate': lambda x: random.uniform(0.5, 3.0),
#         'intr_rate2': lambda x: random.uniform(3.5, 5.0),
#         'save_trm': lambda x: random.randint(6, 36),
#     }
# )

# # Generate saving products
# seeder.add_entity(
#     SavingProducts,
#     10,
#     {
#         'fin_prdt_cd': lambda x: f'SP{x+1}',
#         'kor_co_nm': lambda x: f'Financial Company {x+1}',
#         'fin_prdt_nm': lambda x: f'Saving Product {x+1}',
#         'etc_note': lambda x: f'Description of Saving Product {x+1}',
#         'join_deny': lambda x: random.randint(1, 3),
#         'join_member': lambda x: f'Join Member {x+1}',
#         'join_way': lambda x: f'Join Way {x+1}',
#         'spcl_cnd': lambda x: f'Special Condition {x+1}',
#     }
# )

# # Generate saving options
# seeder.add_entity(
#     SavingOptions,
#     30,
#     {
#         'fin_prdt_cd': lambda x: SavingProducts.objects.get(pk=(x % 10) + 1),
#         'intr_rate_type_nm': lambda x: f'Interest Rate Type {x+1}',
#         'intr_rate': lambda x: random.uniform(0.5, 3.0),
#         'intr_rate2': lambda x: random.uniform(3.5, 5.0),
#         'save_trm': lambda x: random.randint(6, 36),
#     }
# )

# # Execute the seeding process
# inserted_pks = seeder.execute()

# print(f'Seeding completed: {inserted_pks}')



from django.contrib.auth.hashers import make_password
from faker import Faker
import random
from accounts.models import Profile, User

fake = Faker('ko_KR')
# 프로퍼티 되는 버전
# Generate and create 1000 dummy users
for _ in range(1000):
    # Generate dummy data for User instance
    username = fake.user_name()
    realname = fake.name()
    password = make_password(fake.password())
    email = fake.email()
    region = random.choice(['Seoul', 'Gyeonggi', 'Incheon', 'Busan'])
    sex = random.choice(['Male', 'Female'])
    age = random.randint(18, 60)
    income = random.randint(2000, 10000)
    ready_money = random.randint(100, 1000)

    # Create dummy user instance
    dummy_user = User.objects.create(
        username=username,
        realname=realname,
        password=password,
        email=email,
        region=region,
        sex=sex,
        age=age,
        income=income,
        ready_money=ready_money,
    )

    # Generate dummy data for Profile instance
    bio = fake.word()
    avatar = fake.image_url()
    stock_amount = round(random.uniform(1000, 10000), 2)
    stock_access_count = random.randint(0, 100)
    bond_amount = round(random.uniform(1000, 10000), 2)
    bond_access_count = random.randint(0, 100)
    loan_amount = round(random.uniform(1000, 10000), 2)
    loan_access_count = random.randint(0, 100)
    cash_equivalents_amount = round(random.uniform(1000, 10000), 2)
    cash_equivalents_access_count = random.randint(0, 100)
    property_amount = round(
        sum([stock_amount, bond_amount, loan_amount, cash_equivalents_amount]), 2
    )
    cash_hyup_count = random.randint(0, 10)
    cash_content_count = random.randint(0, 10)

    # Create dummy profile instance
    dummy_profile = Profile.objects.create(
        user=dummy_user,
        bio=bio,
        avatar=avatar,
        stock_amount=stock_amount,
        stock_access_count=stock_access_count,
        bond_amount=bond_amount,
        bond_access_count=bond_access_count,
        loan_amount=loan_amount,
        loan_access_count=loan_access_count,
        cash_equivalents_amount=cash_equivalents_amount,
        cash_equivalents_access_count=cash_equivalents_access_count,
        property_amount=property_amount,
        cash_hyup_count=cash_hyup_count,
        cash_content_count=cash_content_count,
    )
