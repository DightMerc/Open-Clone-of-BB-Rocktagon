from rest_framework import serializers
from .models import Users


class UsersSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    full_name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)


    def create(self, validated_data):
        return Users.objects.create(**validated_data)