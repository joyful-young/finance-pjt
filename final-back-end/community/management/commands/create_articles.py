# from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model
# from faker import Faker
# from community.models import Article, Comment
# import random


# class Command(BaseCommand):
#     help = 'Creates dummy articles and comments based on existing users'

#     def handle(self, *args, **options):
#         fake = Faker()
#         User = get_user_model()
#         users = User.objects.all()

#         def generate_random_likes():
#             return random.randint(0, 1000)  # Adjust the range as per your requirement

#         for user in users:
#             for _ in range(random.randint(1, 5)):
#                 article = Article.objects.create(
#                     title=fake.sentence(),
#                     content=fake.paragraph(),
#                     category=fake.word(),
#                     like_count=generate_random_likes(),
#                     write_user=user,
#                     annoymous_is_active=fake.pybool(),  # Randomly assign True or False
#                 )
#                 article.article_like_user.set(random.sample(list(users), random.randint(0, len(users))))

#                 for _ in range(random.randint(0, 3)):
#                     comment = Comment.objects.create(
#                         content=fake.paragraph(),
#                         article=article,
#                         user=random.choice(users),
#                     )
#                     comment.comment_like_user.set(random.sample(list(users), random.randint(0, len(users))))

#         self.stdout.write(self.style.SUCCESS('Dummy data generation completed.'))



from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from community.models import Article, Comment
import random


class Command(BaseCommand):
    help = 'Creates dummy articles and comments based on existing users'

    def handle(self, *args, **options):
        fake = Faker('ko_KR')
        User = get_user_model()
        users = User.objects.all()

        def generate_random_likes():
            return random.randint(0, 1000)  # Adjust the range as per your requirement

        for user in users:
            for _ in range(random.randint(1, 5)):
                article = Article.objects.create(
                    title=fake.sentence(),
                    content=fake.paragraph(),
                    category=fake.word(),
                    like_count=generate_random_likes(),
                    write_user=user,
                    annoymous_is_active=fake.pybool(),  # Randomly assign True or False
                )
                article.article_like_user.set(random.sample(list(users), random.randint(0, len(users))))

                for _ in range(random.randint(0, 3)):
                    comment = Comment.objects.create(
                        content=fake.paragraph(),
                        article=article,
                        user=random.choice(users),
                    )
                    comment.comment_like_user.set(random.sample(list(users), random.randint(0, len(users))))

        self.stdout.write(self.style.SUCCESS('Dummy data generation completed.'))

