from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import index, show_hot, question, thelogin, signup, category, check_answer


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_show_hot_url_resolves(self):
        url = reverse('show_hot')
        self.assertEquals(resolve(url).func, show_hot)

    def test_question_url_resolves(self):
        url = reverse('question', args=[1])  # Здесь вы можете указать любой целочисленный аргумент
        self.assertEquals(resolve(url).func, question)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, thelogin)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEquals(resolve(url).func, signup)

    def test_category_url_resolves(self):
        url = reverse('category', args=['example'])  # Здесь вы можете указать любую строку в качестве аргумента
        self.assertEquals(resolve(url).func, category)

    def test_check_answer_url_resolves(self):
        url = reverse('check_answer')
        self.assertEquals(resolve(url).func, check_answer)
