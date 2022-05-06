from django import forms

from .models import Post, UserReply


class PostForm(forms.ModelForm):
    """Модель формы для создания объявления"""
    class Meta:
        model = Post
        fields = '__all__'
        # __all__ означает, что Django сам должен пойти в модель и взять все поля, кроме
        # первичного ключа (его мы не должны редактировать).
        exclude = ['authorUser', ]  # Исключаем поле authorUser


class UserReplyForm(forms.ModelForm):
    """Модель формы для отклика к конкретному объявлению.
    Эта форма размещается на странице объявления post_detail.
    Автор отклика и id связанного объявления добавляются в методе post представления PostDetailView"""
    class Meta:
        model = UserReply
        fields = ['text', ]

