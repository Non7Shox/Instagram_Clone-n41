from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from postslikesandcomments.models import PostModel, PostCommentModel
from postslikesandcomments.serializers import PostSerializer, CommentSerializer
from shared.custom_pagination import CustomPagination


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return PostModel.objects.all()


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return PostCommentModel.objects.filter(post_id=post_id)


class PostCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        parent_id = serializer.data['parent_id']
        if parent_id:
            serializer.save(parent_id=parent_id)
        post_id = self.kwargs.get('pk')
        serializer.save(user=self.request.user, post_id=post_id)
