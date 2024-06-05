from django.urls import path
from . import views
from .views import UserListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'
urlpatterns = [
    path('create/', views.CreateView.as_view(), name='create'),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),  # 로그인한 사용자 프로필
    path('profile/<int:id>/', views.UserProfileView.as_view(), name='profile_detail'),  # 특정 사용자 프로필
    path('users/', UserListView.as_view(), name='user-list'),
]
