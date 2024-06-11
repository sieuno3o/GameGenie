from django.urls import path
from . import views
from .views import CategoryListView

app_name = 'community'
urlpatterns = [
    path('', views.CommunityList.as_view(), name='list'),  # 게시글 조회
    path('create/', views.CommunityCreate.as_view(), name='create'),  # 게시글 생성
    path('<int:pk>/', views.CommunityDetail.as_view(), name='detail'),  # 게시글 조회, 수정, 삭제
    path('<int:pk>/like/', views.CommunityLike.as_view(), name='like'),  # 게시글 좋아요
    path('<int:community_pk>/comments/create/', views.CommentCreate.as_view(), name='comment_create'),  # 댓글 생성
    path('<int:community_pk>/comments/', views.CommentsList.as_view(), name='comment_list'),  # 댓글 목록 조회
    path('<int:community_pk>/comments/<int:comment_id>/',
         views.CommentDetail.as_view(), name='comment_detail'),  # 댓글 조회, 수정, 삭제
    path('comments/<int:comment_id>/like/', views.CommentLike.as_view(), name='comment_like'),  # 댓글 좋아요
    path('comments/user/<int:pk>/', views.UserCommentsList.as_view(), name='comment_user_list'),  # 유저가 작성한 댓글
    path('replies/<int:comment_id>/', views.ReplyList.as_view(), name='reply-list'),  # 대댓글 조회
    path('replies/<int:comment_id>/create/', views.ReplyCreate.as_view(), name='reply-create'),  # 대댓글 생성
    path('replies/<int:comment_id>/<int:reply_id>/', views.ReplyDetail.as_view(), name='reply-update'),  # 대댓글 수정, 삭제
    path('replies/<int:reply_id>/like/', views.ReplyLike.as_view(), name='reply-like'),  # 대댓글 좋아요
    path('search/', views.CommunitySearch.as_view(), name='search'),  # 검색 및 필터 뷰
    path('categories/', CategoryListView.as_view(), name='category-list'),  # 카테고리
]
