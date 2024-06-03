from rest_framework import serializers
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'game_name', 'game_image', 'game_review', 'game_price', 'game_url']
        read_only_fields = ['user']
