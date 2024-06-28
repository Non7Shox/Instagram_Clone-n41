from rest_framework import generics, status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserModel, ConfirmationModel, CODE_VERIFIED, DONE, PHOTO
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.serializers import SignUpSerializer, UpdateUserSerializer, UserAvatarSerializer


class SignUpCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    model = UserModel


class VerifyCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = request.data.get('code')

        verification_code = ConfirmationModel.objects.filter(
            user_id=user.id, code=code, is_confirmed=False, expiration_time__gte=timezone.now())
        if verification_code.exists():
            user.auth_status = CODE_VERIFIED
            user.save()

            verification_code.update(is_confirmed=True)

            response = {
                'success': True,
                'message': "Your code is successfully verified.",
                'auth_status': CODE_VERIFIED,
                'access_token': user.tokens()['access_token']
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'success': False,
                'message': "Your code is invalid or already expired"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UpdateUserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            user.auth_status = DONE
            user.save()

            response = {
                "success": True,
                "message": "Updated successfully",
                "auth_status": DONE,
                "access_token": user.tokens()['access_token'],
                "refresh_token": user.tokens()['refresh_token']
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        else:
            response = {
                "success": False,
                "message": "Invalid request body",
                "errors": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAvatarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserAvatarSerializer(data=request.data)

        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            user.auth_status = PHOTO
            user.save()

            response = {
                "success": True,
                "message": "Updated successfully",
                "auth_status": PHOTO,
            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        else:
            response = {
                "success": False,
                "message": "Invalid request",
                "errors": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
