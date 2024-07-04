from django.urls import path

from postslikesandcomments.views import PostListView, PostCreateView, PostCommentListView, PostCommentCreateAPIView

app_name = 'postslikesandcomments'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>/comments/', PostCommentListView.as_view(), name='comments-list'),
    path('<int:pk>/comments/create/', PostCommentCreateAPIView.as_view(), name='comments-create')
]
