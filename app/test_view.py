from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, Category, Rating, Profile


class ViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.user.set_password('test_password')
        self.user.save()
        self.profile = Profile.objects.create(nickname='test_user', user=self.user)
        self.category = Category.objects.create(title='Test Category')
        self.question = Question.objects.create(text='Test Question', category=self.category, answer='Test Answer')

    def test_index_view(self):
        login = self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'themain.html')

    def test_question_view(self):
        login = self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('question', kwargs={'q_id': self.question.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thequestion.html')

    def test_check_answer_view(self):
        login = self.client.login(username='test_user', password='test_password')
        response = self.client.post(reverse('check_answer'),
                                    {'InputName': 'Test Answer', 'question_id': self.question.id, 'markQInput': 1})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('question', kwargs={'q_id': self.question.id}))

    def test_category_view(self):
        login = self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('category', kwargs={'cat_id': self.category.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thecategory.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thelogin.html')

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)

        # Проверяем, что не используется никакой шаблон (None)
        self.assertEqual(response.templates, [])

