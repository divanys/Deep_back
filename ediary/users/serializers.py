from rest_framework import serializers
from .models import Group  # Импортируем модель

class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group"""
    class Meta:
        model = Group
        fields = "__all__"  # Выбираем, какие поля будут в JSON (можно ["id", "name"])