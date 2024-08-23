from django.contrib.auth.models import User
from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from portfolio.models import Portfolio
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True,
                                       min_value=Decimal(100.00), max_value=Decimal(10000.00),
                                       default=Decimal(100.00))

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'balance')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        with transaction.atomic():
            balance = validated_data.pop('balance', Decimal(100.00))
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            user.save()

            # Create the profile
            profile = Profile.objects.create(user=user, balance=balance)

            # Create the portfolio
            Portfolio.objects.create(profile=profile, balance=balance, equity=balance)

            return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('id', 'username', 'balance', 'realized_pl')

    balance = serializers.DecimalField(max_digits=7, decimal_places=2, min_value=Decimal(100.00),
                                       max_value=Decimal(1000.00))
