from django.contrib import admin
from .models import PostModel, PostLikeModel, PostCommentModel, CommentLikeModel


@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'updated_at')
    search_fields = ('caption', 'user__username')
    list_filter = ('created_at', 'updated_at')


@admin.register(PostLikeModel)
class PostLikeModelAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('user__username', 'post__caption')
    list_filter = ('created_at',)


@admin.register(PostCommentModel)
class PostCommentModelAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'comment', 'created_at', 'parent')
    search_fields = ('comment', 'user__username', 'post__caption')
    list_filter = ('created_at',)


@admin.register(CommentLikeModel)
class CommentLikeModelAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'created_at')
    search_fields = ('user__username', 'comment__comment')
    list_filter = ('created_at',)