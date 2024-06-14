from django.shortcuts import render
from django.http import HttpResponse
import math
import json
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control

from .forms import LoginForm, CommentForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
import random
from django.db import IntegrityError
from .models import Question, Rating, Category, Profile, Comment
from .forms import LoginForm, RegisterForm
from django.utils.translation import gettext as _
# Create your views here.

word_list = Category.objects.all()
word_ad=''
word_ad1=''
quest=Question.objects.new_questions_list()
questions = []
for i in range(0, 80, 2):
    if (quest[i].category.title == "Переведи!"):
        word_ad='/logic.png'
    elif (quest[i].category.title == "Найди лишнее слово"):
        word_ad = '/extra1.jpg'
    elif (quest[i].category.title == "Математика"):
        word_ad = '/math.jpg'
    else:
        word_ad = '/word.jpg'
    if (quest[i+1].category.title == "Переведи!"):
        word_ad1='/logic.png'
    elif (quest[i+1].category.title == "Найди лишнее слово"):
        word_ad1 = '/extra1.jpg'
    elif (quest[i+1].category.title == "Математика"):
        word_ad1= '/math.jpg'
    else:
        word_ad1 = '/word.jpg'

    questions.append([
        {
            'id': quest[i].id,
            'name': quest[i].category.title,
            'title': f'Вопрос из раздела {quest[i].category.title}',
            'ct_id': quest[i].category.title,
            'content': f'{quest[i].text}',
            'ad': word_ad,
            'kol': quest[i].ratingQ_count
        },
        {
            'id': quest[i+1].id,
            'name': quest[i+1].category.title,
            'title': f'Вопрос из раздела {quest[i+1].category.title}',
            'ct_id': quest[i+1].category.title,
            'content': f'{quest[i+1].text}',
            'ad': word_ad1,
            'kol': quest[i+1].ratingQ_count
        }
    ])


quest1=Question.objects.hot_questions_list()
questions1 = []
for i in range(0, 80, 2):
    if (quest1[i].category.title == "Переведи!"):
        word_ad='/logic.png'
    elif (quest1[i].category.title == "Найди лишнее слово"):
        word_ad = '/extra1.jpg'
    elif (quest1[i].category.title == "Математика"):
        word_ad = '/math.jpg'
    else:
        word_ad = '/word.jpg'
    if (quest1[i+1].category.title == "Переведи!"):
        word_ad1='/logic.png'
    elif (quest1[i+1].category.title == "Найди лишнее слово"):
        word_ad1 = '/extra1.jpg'
    elif (quest1[i+1].category.title == "Математика"):
        word_ad1= '/math.jpg'
    else:
        word_ad1 = '/word.jpg'

    questions1.append([
        {
            'id': quest1[i].id,
            'name': quest1[i].category.title,
            'title': f'Вопрос из раздела {quest1[i].category.title}',
            'ct_id': quest1[i].category.title,
            'content': f'{quest1[i].text}',
            'ad': word_ad,
            'kol': quest1[i].ratingQ_count
        },
        {
            'id': quest1[i+1].id,
            'name': quest1[i+1].category.title,
            'title': f'Вопрос из раздела {quest1[i+1].category.title}',
            'ct_id': quest1[i+1].category.title,
            'content': f'{quest1[i+1].text}',
            'ad': word_ad1,
            'kol': quest1[i+1].ratingQ_count
        }
    ])

hu=Profile.objects.hot_users()
hot_users=[]
for i in range(1, 6):
    if (hu[i].ratingP_count is not None):
        hot_users.append([hu[i].nickname, hu[i].ratingP_count])

def paginate(objects, page, per_page=2):
    paginator = Paginator(objects, per_page)
    obj = paginator.get_page(page)
    return obj


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login/', redirect_field_name='continue')
def index(request):
    name=request.user.profile.nickname
    page = request.GET.get('page')
    if not page:
        page = 1
    return render(request, 'themain.html', {'questionpair': paginate(questions, int(page)), 'hot_users':hot_users, 'name':name})

def thelogin(request):
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            user = authenticate(request, **login_form.cleaned_data)
            print("SUCCESS1")
            if user is not None:
                login(request, user)
                print("SUCCESS2")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Неверный пароль или такого пользователя не существует")

    return render(request, 'thelogin.html', context={'form':login_form, 'hot_users':hot_users})

def signup(request):

    if request.method == "GET":
        signup_form = RegisterForm()
    elif request.method == "POST":
        signup_form = RegisterForm(request.POST, request.FILES)
        print("SUCCESS0")
        if signup_form.is_valid():
            print("SUCCESS1")
            try:
                user = signup_form.save()
                print("SUCCESS2")
                login(request, user)
                return redirect(reverse('index'))
            except IntegrityError:
                signup_form.add_error(None, _('Пользователь с таким именем уже существует.'))
                print("SUCCESS3")
    else:
        signup_form = RegisterForm()

    return render(request, 'thesignup.html', context={'form': signup_form, 'hot_users':hot_users})


def question(request, q_id):
    element = next((item for sublist in questions for item in sublist if item['id'] == q_id), None)
    comments = Comment.objects.comments_list(q_id)
    name = request.user.profile.nickname
    user_id = request.user.profile.id
    comments_user = Comment.objects.filter(profile_id=user_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(request, q_id)
            return redirect(reverse('question', kwargs={'q_id': q_id}))
    else:
        form = CommentForm()

    return render(request, 'thequestion.html', {'question': element,  'comments':comments, 'hot_users':hot_users, 'name':name,  'form': form, 'comments_user':comments_user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login/', redirect_field_name='continue')
def show_hot(request):
    name = request.user.profile.nickname
    sh = True
    page = request.GET.get('page')
    if not page:
        page = 1
    return render(request, 'themain.html', {'questionpair': paginate(questions1, int(page)), 'sh':sh, 'hot_users':hot_users, 'name':name})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login/', redirect_field_name='continue')
def category(request, cat_id):
    name = request.user.profile.nickname
    filtered_questions = []
    pair = []
    for question_set in questions:
        for quest in question_set:
            if quest['ct_id'] == cat_id:
                pair.append(quest)
                if len(pair) == 2:
                    filtered_questions.append(pair)
                    pair = []

    page = request.GET.get('page')
    if not page:
        page = 1
    return render(request, "thecategory.html", {'catquest': paginate(filtered_questions, int(page)), 'hot_users':hot_users, 'name':name})


@login_required(login_url='login/', redirect_field_name='continue')
def check_answer(request):
    if request.method == 'POST':
        user_answer = request.POST.get('InputName')
        question_id = request.POST.get('question_id')

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            messages.error(request, _('Вопрос не найден.'))
            return redirect('index')

        correct_answer = question.answer

        # Определение правильности ответа
        if user_answer.lower() == correct_answer.lower():
            markU = 1
            messages.success(request, _('Правильный ответ!'))
        else:
            markU = 0
            messages.error(request, _('Неправильный ответ!'))

        # Определение значения markQ (лайк пользователя)
        markQ = int(request.POST.get('markQInput', 0))


        # Создание объекта Rating и сохранение в базу данных
        # Проверяем, был ли оценен данный вопрос пользователем
        rating = Rating.objects.filter(question=question, prof=request.user.profile).first()
        if rating:
            # Если оценка уже существует, обновляем значение markQ в соответствии с переданным значением
            rating.markQ = markQ
            rating.markU = markU
            rating.save()
        else:
            # Если оценка не существует, создаем новый объект Rating
            rating = Rating(question=question, prof=request.user.profile, markQ=markQ, markU=markU)
            rating.save()

        return redirect('question', q_id=question_id)

    return render(request, 'thequestion.html')


def delete_comment(request, comment_id):
    print("In view")
    if request.method == 'DELETE':
        print('Delete comment view function called, commentId:', comment_id)
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def update_comment(request, comment_id):
    if request.method == 'PUT':
        print('update comment view function called, commentId:', comment_id)
        comment = Comment.objects.get(pk=comment_id)
        data = json.loads(request.body.decode('utf-8'))  # parse JSON data from request body
        new_text = data.get('text')
        comment.text = new_text
        comment.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def exit(request):
    print("Kek")
    logout(request)
    return redirect(reverse('login'))