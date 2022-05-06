from django.contrib import admin
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Post, UserReply, Category


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['authorUser', ]  # убираем поле в админке, чтобы не редактировать


class UserReplyAdminForm(forms.ModelForm):

    class Meta:
        model = UserReply
        fields = '__all__'
        exclude = ['userReply', ]  # убираем поле в админке, чтобы не редактировать


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели
        """
        if not change:  # Проверяем что запись только создаётся
            obj.authorUser = request.user  # Присваеваем полю автор текущего пользователя

        super(PostAdmin, self).save_model(
            request=request,
            obj=obj,
            form=form,
            change=change
        )


class UserReplyAdmin(admin.ModelAdmin):
    form = UserReplyAdminForm

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод сохранения модели
        """
        if not change:  # Проверяем что запись только создаётся
            obj.userReply = request.user  # Присваеваем полю автор текущего пользователя

        super(UserReplyAdmin, self).save_model(
            request=request,
            obj=obj,
            form=form,
            change=change
        )


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(UserReply, UserReplyAdmin)

