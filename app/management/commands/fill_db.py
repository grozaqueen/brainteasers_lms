from django.core.management import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random
import os

from app.models import Profile, Rating, Question, Category

fake = Faker()


class Command(BaseCommand):
    help = 'Filling Database'

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['num']
        rate = 10

        users = [
            User(
                username=fake.unique.user_name()[:fake.random_int(min=3, max=8)] + fake.unique.user_name()[
                                                                                   :fake.random_int(min=3,
                                                                                                    max=7)] + f'{fake.random_int(min=0, max=1000)}',

                password=fake.password(special_chars=False),
                first_name=fake.first_name(),
                last_name=fake.last_name()
            ) for i in range(num)
        ]
        User.objects.bulk_create(users)
        self.stdout.write("Finished with users")
        users = User.objects.all()

        profiles = [
            Profile(
                user=users[i],
                nickname=fake.first_name() + '_' + fake.last_name()
            ) for i in range(num)
        ]
        Profile.objects.bulk_create(profiles)
        self.stdout.write("Finished with profiles")
        profiles = Profile.objects.all()

        categories = ['Найди лишнее слово', 'Угадай слово', 'Математика', 'Переведи!']
        categories_objs = [
            Category(title=category)
            for category in categories
        ]
        Category.objects.bulk_create(categories_objs)

        self.stdout.write("Finished with categories")
        categories = Category.objects.all()

        questions_per_category = 20

        question_files = [
            "app/management/commands/extra.txt",
            "app/management/commands/word.txt",
            "app/management/commands/maths.txt",
            "app/management/commands/logic.txt"
        ]
        answer_files = [
            "app/management/commands/extraans.txt",
            "app/management/commands/wordans.txt",
            "app/management/commands/mathans.txt",
            "app/management/commands/logicans.txt"
        ]

        questions = []
        for i, category in enumerate(categories):
            with open(question_files[i], "r") as question_file:
                with open(answer_files[i], "r") as answer_file:
                    lines = list(zip(question_file.readlines(), answer_file.readlines()))
                    random.shuffle(lines)

            category_questions = [
                Question(
                    text=line[0].strip(),
                    answer=line[1].strip(),
                    date=str(fake.date_time_this_decade()),
                    category=category
                ) for line in lines
            ]
            questions.extend(category_questions)

        random.shuffle(questions)
        Question.objects.bulk_create(questions)
        self.stdout.write("Finished with questions")

        questions = Question.objects.all()

        question_ratings = [
            Rating(
                markQ=0 if fake.random_int(min=0, max=100) % 4 == 0 else 1,
                markU=0 if fake.random_int(min=0, max=100) % 4 == 0 else 1,
                prof=profiles[fake.random_int(min=0, max=num - 1)],
                question=questions[i] if i < len(questions) else questions[
                    fake.random_int(min=0, max=len(questions) - 1)]
            ) for i in range(num * 2 * rate)
        ]
        Rating.objects.bulk_create(question_ratings)
        self.stdout.write("Finished with Question ratings")
