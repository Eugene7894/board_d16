from django_filters import FilterSet, ModelChoiceFilter, TypedChoiceFilter, NumberFilter
from distutils.util import strtobool

from .models import Post, UserReply, Category

BOOLEAN_CHOICES = (('False', 'Не принято'), ('True', 'Принято'),)


class PostsListFilter(FilterSet):
    """Выбираем в фильтрах категорию из модели Category"""
    postCategory = ModelChoiceFilter(label='Категории',
                                     queryset=Category.objects.all()
                                     )

    class Meta:
        model = Post
        fields = ('postCategory',)


class UserReplyFilter(FilterSet):
    """Выбираем статус отклика, для полей is_accepted и postReply_id указываем имена в фильтрах"""
    is_accepted = TypedChoiceFilter(label='Статус отклика',
                                    choices=BOOLEAN_CHOICES,
                                    coerce=strtobool
                                    )
    postReply_id = NumberFilter(label='ID объявления')

    class Meta:
        model = UserReply
        fields = ('postReply_id', 'is_accepted', )
