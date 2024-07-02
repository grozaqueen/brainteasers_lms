from django.db import models
from django.conf import settings
from django.db.models import Sum

class ProfileManager(models.Manager):
    def find_profile(self, user_id):
        return self.filter(user=user_id).first()

    def hot_users(self):
        return self.annotate(total_rating=Sum('rating__markU')).order_by('-total_rating')

class Profile(models.Model):
    def ratingP_count(self):
        r_sum = Rating.objects.filter(prof=self).aggregate(Sum('markU'))
        return r_sum['markU__sum']

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default='avatar.jpg', upload_to='avatar/%Y/%m/%d')
    nickname = models.CharField(max_length=30)
    objects = ProfileManager()


class Category(models.Model):
    title = models.CharField(max_length=30)


class QuestionManager(models.Manager):
    def new_questions_list(self):
        return self.order_by('date').reverse()

    def find_by_category(self, category_name):
        return self.prefetch_related('category').filter(category__title=category_name)


class Question(models.Model):
    def ratingQ_count(self):
        r_sum = Rating.objects.filter(question=self).aggregate(Sum('markQ'))
        return r_sum['markQ__sum']

    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    answer = models.CharField(max_length=30)

    objects = QuestionManager()


class Rating(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    prof = models.ForeignKey(Profile, on_delete=models.CASCADE)
    markQ = models.IntegerField()
    markU = models.IntegerField()

class CommentManager(models.Manager):
    def comments_list(self, question_id):
        return self.filter(question=question_id).order_by('-date')

class Comment(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()