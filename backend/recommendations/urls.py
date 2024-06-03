from django.urls import path
from .views import GameViewSet, FavoriteCreateView, FavoriteDeleteView, FavoriteListView

urlpatterns = [
    path('games/', GameViewSet.as_view({'get': 'list'}), name='game-list'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-add'),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
]
