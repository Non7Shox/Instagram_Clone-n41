from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from shared.utils import send_code_to_email, send_code_to_phone
from users.models import UserModel, VIA_EMAIL, VIA_PHONE


class SignUpSerializer(serializers.ModelSerializer):
    email_phone_number = serializers.CharField(max_length=128, required=True)

    uuid = serializers.IntegerField(read_only=True)
    auth_type = serializers.CharField(read_only=True, required=False)
    auth_status = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = UserModel
        fields = ['uuid', 'email_phone_number', 'auth_type', 'auth_status']

    def validate(self, data):
        data = self.auth_validate(data=data)
        auth_type = data['auth_type']
        if auth_type == VIA_EMAIL:
            if UserModel.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("This email is already registered, use resend code API.")
        else:
            if UserModel.objects.filter(phone_number=data['phone_number']).exists():
                raise serializers.ValidationError("This phone number is already registered, use resend code API.")
        return data

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        code = user.create_verify_code(user.auth_type)

        if user.auth_type == VIA_EMAIL:
            send_code_to_email(user.email, code)
        else:
            send_code_to_phone(phone_number=user.phone_number, code=code)
        user.save()
        return user

    @staticmethod
    def auth_validate(data):
        user_input = str(data['email_phone_number']).lower()
        if user_input.endswith('@gmail.com'):
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL
            }
        elif user_input.startswith("+"):
            data = {
                'phone_number': user_input,
                'auth_type': VIA_PHONE
            }
        else:
            data = {
                'success': False,
                'message': "Please enter a valid phone number or email"
            }
            raise serializers.ValidationError(data)
        return data

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data['access_token'] = instance.tokens()['access_token']
        return data


class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True, required=False)
    confirm_password = serializers.CharField(max_length=128, write_only=True, required=False)

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password or confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError("Passwords don't match")
            # TODO: Add additional password validations (min length, numbers and letters)

        return data

    def validate_username(self, username):
        if UserModel.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username is already taken")
        return username

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))

        instance.save()
        return instance


class UserAvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField(validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])])

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance
