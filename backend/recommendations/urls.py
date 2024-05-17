from django.urls import path
from .views import GameViewSet

game_list = GameViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('', game_list, name='game-list'),
]
