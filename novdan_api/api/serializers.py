from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from oauth2_provider.models import get_refresh_token_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as RestValidationError

from .models import Wallet

User = get_user_model()
RefreshToken = get_refresh_token_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise RestValidationError({ 'email': ['User with this email already exists.'] })

        if User.objects.filter(username=data['username']).exists():
            raise RestValidationError({ 'username': ['User with this username already exists.'] })

        try:
            validate_password(data['password'], User(email=data['email'], username=data['username']))
        except DjangoValidationError as validation_error:
            raise RestValidationError({ 'password': validation_error.messages })

        if data['password'] != data['confirm_password']:
            raise RestValidationError({ 'confirm_password': ['Passwords do not match.'] })

        return data

    def create(self, validated_data):
        new_user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        new_user.set_password(validated_data['password'])
        new_user.save()

        return new_user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise RestValidationError('The password is not correct.')
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        validate_password(value, user)
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise RestValidationError({ 'confirm_password': ['Passwords do not match.'] })
        return data

    def update(self, instance, validated_data):
        # revoking the refresh token also revokes the associated access token
        for refresh_token in RefreshToken.objects.filter(user=instance):
            refresh_token.revoke()

        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'amount')


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'full_name')
