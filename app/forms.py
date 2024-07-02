from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
import re

from app.models import Profile, Comment, Question


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите никнейм'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль', 'minlength': '6'}),
    )

class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputLogin',
                                      'placeholder': 'Логин для входа в аккаунт'}),
        max_length=15,
        label='Логин', required=True)
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'InputEmail', 'placeholder': 'Адрес электронной почты'}),
        max_length=40,
        label='Эл. почта', required=True, help_text='Формат почты: example@example.com')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'InputPassword'}), max_length=30, min_length=6,
        label='Пароль', required=True, help_text='Минимальная длина пароля - 6 символов.')
    password_check = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'InputPasswordAgain'}), max_length=30,
        min_length=6,
        label='Повторите пароль', required=True)
    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'InputNickname', 'placeholder': 'Отображаемое имя'}),
        max_length=30,
        label='Никнейм',
        required=True
    )

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if nickname:
            pattern = r'^[\w.-]*$'
            if not re.match(pattern, nickname):
                raise forms.ValidationError('В имени пользователя обнаружены недопустимые символы.')
        return nickname

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')

        if password != password_check:
            self.add_error('password_check', 'Введенные пароли не совпадают.')
            raise ValidationError('Введенные пароли не совпадают.')

        username = cleaned_data.get('username')
        nickname = cleaned_data.get('nickname')

        if re.fullmatch(r'(\d|\w|_|-|\.)*', username) or re.fullmatch(r'(\d|\w|_|-|\.)*', username):
            return cleaned_data
        else:
            self.add_error(None, 'В логине или никнейме обнаружены недопустимые символы.')
            raise ValidationError(self)


    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        nickname = self.cleaned_data['nickname']
        avatar = self.cleaned_data['avatar']
        user_profile = Profile(nickname=nickname, avatar=avatar, user=user)
        user_profile.save()
        return user

class CommentForm(forms.ModelForm):

    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control border-secondary', 'id': 'InputText',
                                     'placeholder': 'Введите текст комментария', 'rows': 5}), max_length=500,
        min_length=1,
        required=True)

    class Meta:
        model = Comment
        fields = ['text']

    def save(self, request, question_id, **kwargs):
        text = self.cleaned_data['text']
        question = Question.objects.filter(pk=question_id).first()
        profile = request.user.profile
        date = datetime.now()
        comment = Comment(text=text, question=question, profile=profile, date=date)
        comment.save()
        return comment