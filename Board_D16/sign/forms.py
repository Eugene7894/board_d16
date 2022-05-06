from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OTPC0deForm(forms.Form):
    """Форма ввода одноразового пароля"""
    code = forms.IntegerField(label='Введите код')


class BaseRegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя"""
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("email",
                  "password1",
                  "password2",)
