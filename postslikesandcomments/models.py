from django.db import models
from shared.models import BaseModel
from users.models import UserModel


class PostModel(BaseModel):
    image = models.ImageField(upload_to='postslikesandcomments/')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='postslikesandcomments')
    caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ['created_at']
        db_table = 'postslikesandcomments'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class PostLikeModel(BaseModel):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='post_likes')

    def __str__(self):
        return self.user.full_name

    class Meta:
        db_table = 'post_likes'
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'


class PostCommentModel(BaseModel):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='post_comments')
    comment = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'post_comments'
        verbose_name = 'Post comment'
        verbose_name_plural = 'Post comments'


class CommentLikeModel(BaseModel):
    comment = models.ForeignKey(PostCommentModel, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comment_likes')

    def __str__(self):
        return self.comment.comment

    class Meta:
        db_table = 'comment_likes'
        verbose_name = 'Comment like'
        verbose_name_plural = 'Comment likes'
