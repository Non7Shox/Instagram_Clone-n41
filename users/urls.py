from django.urls import path
from users.views import (SignUpCreateAPIView, CodeVerifyAPIView, ResendCodeVerifyAPIView, UpdateUserAPIView,
                         UpdateAvatarApiView,
                         LoginView,
                         LogoutView,
                         RefreshTokenView,
                         ForgetPasswordView)

app_name = 'users'

urlpatterns = [
    path('register/', SignUpCreateAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('verify/', CodeVerifyAPIView.as_view(), name='verify'),
    path('verify/resend/', ResendCodeVerifyAPIView.as_view(), name='verify-resend'),
    path('update/', UpdateUserAPIView.as_view(), name="update"),
    path('update/avatar/', UpdateAvatarApiView.as_view(), name="update-avatar"),
    path('forget/password/', ForgetPasswordView.as_view(), name="forget-password"),
]
