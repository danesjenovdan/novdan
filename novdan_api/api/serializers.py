from django.contrib.auth.password_validation import validate_password
from oauth2_provider.models import get_refresh_token_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Wallet

RefreshToken = get_refresh_token_model()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError('The password is not correct.')
        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        validate_password(value, user)
        return value

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
