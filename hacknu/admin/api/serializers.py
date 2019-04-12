from rest_framework import serializers
from .models import TelegramUser
from .models import Book


class UsersSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    full_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    phone = serializers.IntegerField()


    def create(self, validated_data):
        return TelegramUser.objects.create(**validated_data)


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=511)
    author = serializers.CharField(max_length=511)
    description = serializers.CharField()
    published_date = serializers.IntegerField()
    rating = serializers.IntegerField()


    def create(self, validated_data):
        return Book.objects.create(**validated_data)