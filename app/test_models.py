import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from app.models import Profile, Question, Category, Rating


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.profile = Profile.objects.create(nickname='test_user', user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.nickname, 'test_user')


    def testfindprofile(self):
        profile = Profile.objects.find_profile(self.user.id)
        self.assertEqual(profile.user.id, self.user.id)

    def testhotusers(self):
        hotusers = Profile.objects.hot_users()
        self.assertIsNotNone(hotusers)

class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.profile = Profile.objects.create(nickname='test_user', user=self.user)

    def testratingQcount(self):
        category = Category.objects.create(title='TestCategory')
        question = Question.objects.create(text='Test Question', category=category, answer='Test Answer')
        rating = Rating.objects.create(prof=self.profile, question=question, markQ=0, markU=0)
        self.assertEqual(question.ratingQ_count(), 0)

    def testnewquestionslist(self):
        newquestions = Question.objects.new_questions_list()
        self.assertIsNotNone(newquestions)

    def testhotquestionslist(self):
        hotquestions = Question.objects.hot_questions_list()
        self.assertIsNotNone(hotquestions)

    def testfindbycategory(self):
        questions = Question.objects.find_by_category('Переведи!')
        for question in questions:
            self.assertEqual(question.category.title, 'Переведи!')
