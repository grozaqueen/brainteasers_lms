from django.contrib import admin
from django.urls import path
from app import views

from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show_hot', views.show_hot, name='show_hot'),
    path('question/<int:q_id>', views.question, name = 'question'),
    path('login/', views.thelogin, name = 'login'),
    path('signup', views.signup, name = 'signup'),
    path('category/<str:cat_id>', views.category, name = 'category'),
    path('check_answer', views.check_answer, name='check_answer'),
    path('admin/', admin.site.urls),
]
