from django.urls import path
from users.views import SignUpCreateAPIView, VerifyCodeAPIView, UpdateUserAPIView, UpdateUserAvatarAPIView

app_name = 'users'

urlpatterns = [
    path('register/', SignUpCreateAPIView.as_view(), name='register'),
    path('verify/', VerifyCodeAPIView.as_view(), name='verify'),
    path('update/', UpdateUserAPIView.as_view(), name='update'),
    path('update/avatar/', UpdateUserAvatarAPIView.as_view(), name='update-avatar'),
]
