from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserReplyListView, \
    reply_delete, reply_accept

urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('post/add_new', PostCreateView.as_view(), name='add_post'),
    path('post/<int:pk>/edit', PostUpdateView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='delete_post'),
    path('replies/', UserReplyListView.as_view(), name='users_replies'),
    path('del_reply/<int:pk>', reply_delete, name='del_reply'),
    path('reply_accept/<int:pk>', reply_accept, name='reply_accept'),
]
