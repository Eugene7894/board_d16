from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, UserReply
from .filters import PostsListFilter, UserReplyFilter
from .forms import PostForm, UserReplyForm


class PostListView(ListView):
    """Вывод всех объявлений, главная страница"""
    model = Post
    template_name = 'board_app/posts.html'
    context_object_name = 'posts'
    ordering = ['-creationDate']
    paginate_by = 3

    def get_queryset(self):
        """Такой способ позволит исп. вместе и фильтрацию, и пагинацию.
        Не нужно в шаблоне итерироваться по posts_filter.qs"""
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostsListFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем фильтр постов PostsListFilter в контекст, чтобы добавить форму поиска в шаблон
        context['posts_filter'] = self.filterset
        return context


class PostDetailView(DetailView):
    """Вывод конкретного объявления"""
    model = Post
    template_name = 'board_app/post_detail.html'
    context_object_name = 'post'

    # Добавляем нашу форму для откликов в контекст(переменная для шаблона)
    form = UserReplyForm
    extra_context = {'form': UserReplyForm}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        if self.request.user.id:
            context['user_post_reply'] = UserReply.objects.filter(userReply=self.request.user, postReply=pk).exists()
        return context

    def post(self, request, *args, **kwargs):
        """При отправки формы выполнить следующий код
        form.instance - для автоматического заполнения (переопределения) полей формы
        instance - типа данный объект, вроде self, но со своими особенностями"""
        form = UserReplyForm(request.POST)
        if form.is_valid():
            form.instance.postReply_id = self.kwargs.get('pk')
            form.instance.userReply = self.request.user
            form.save()

            # Ссылка перехода на ту же самую страницу после выполнения POST-запроса.
            return redirect(request.META.get('HTTP_REFERER'))


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание нового объявления"""
    model = Post
    template_name = 'board_app/add_post.html'
    form_class = PostForm

    def form_valid(self, form):
        """Автозаполнение поля authorUser"""
        form.instance.authorUser = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование объявления"""
    model = Post
    template_name = 'board_app/add_post.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        """Метод заполняет форму на странице add_post.html текущим объявлением,
        чтобы пользователь мог отредактировать необходимую информацию"""
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление объявления"""
    model = Post
    template_name = 'board_app/delete_post.html'
    # queryset - переопределение вывода информации на страницу
    queryset = Post.objects.all()
    # success_url - перенаправление на url с name = 'posts'
    success_url = reverse_lazy('posts')
    # Если мы используем success_url, мы должны использовать reverse_lazy() 2. Если мы реверсируем внутри функции,
    # мы можем использовать reverse().


class UserReplyListView(LoginRequiredMixin, ListView):
    """Вывод всех откликов на объявления автора"""
    model = UserReply
    template_name = 'board_app/users_replies.html'
    context_object_name = 'users_replies'
    ordering = ['-creationDate']
    paginate_by = 5

    def get_queryset(self, **kwargs):
        """Создаем queryset для представления для откликов пользователей в контексте
        объявлений автора объявлений"""
        authoruser_id = self.request.user.id
        queryset = UserReply.objects.filter(postReply__authorUser=authoruser_id).order_by('-creationDate')
        self.filterset = UserReplyFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров, что позволит итерироваться в шаблоне по
        # context_object_name, а не reply_filter.qs.
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем фильтр постов UserReplyFilter в контекст, чтобы добавить форму поиска в шаблон
        context['reply_filter'] = self.filterset
        return context


@login_required
def reply_delete(request, **kwargs):
    """Функция-представления для удаления отклика"""
    user_reply_id = kwargs.get('pk')
    UserReply.objects.get(pk=user_reply_id).delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def reply_accept(request, **kwargs):
    """Функция-представления для принятия отклика"""
    user_reply_id = kwargs.get('pk')
    user_reply = UserReply.objects.get(pk=user_reply_id)
    user_reply.is_accepted = True
    user_reply.save()

    return redirect(request.META.get('HTTP_REFERER'))



