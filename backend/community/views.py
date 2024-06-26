from rest_framework.response import Response
from .filters import CommunityFilter
from community.serializers import CommunitySerializer, CommentSerializer, ReplySerializer
from community.models import Community, Comment, Reply
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from accounts.models import User
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.http import JsonResponse
from .serializers import CategorySerializer
from rest_framework.pagination import PageNumberPagination
from django.utils.html import escape

class CommuityListPagination(PageNumberPagination):
    page_size = 10

class CommentsListPagination(PageNumberPagination):
    page_size = 5



class CommunityList(ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['created_at', 'likes_count', 'views_count']
    search_fields = ['title', 'content', 'author__username']
    pagination_class = CommuityListPagination
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Community.objects.annotate(
            community_like_count=Count('community_like'),
            comments_count=Count('comments')  # 댓글 수를 계산하여 추가
        )
        ordering = self.request.query_params.get('ordering', 'created_at')
        if ordering == 'community_like_count':
            queryset = queryset.order_by('-community_like_count')
        return queryset


class CommunityCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id

        # 데이터 정규화 및 유효성 검사
        serializer = CommunitySerializer(data=data)
        if serializer.is_valid():
            community = serializer.save(author=request.user)
            response_data = {
                "message": "등록완료",
                "communityId": community.id
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommunityDetail(APIView):
    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        community.view_count += 1  # 조회수 증가
        community.save()
        serializer = CommunitySerializer(community)
        return Response(serializer.data)

    def patch(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = CommunitySerializer(community, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "수정완료"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        community.delete()
        return Response({"message": "삭제완료"}, status=status.HTTP_204_NO_CONTENT)


class CommunityLike(generics.UpdateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if instance.is_liked_by_user(user):
            instance.unlike(user)
            liked = False
        else:
            instance.like(user)
            liked = True

        instance.save()

        likes_count = instance.get_likes_count()

        return Response({'liked': liked, 'likes_count': likes_count}, status=status.HTTP_200_OK)


class CommentCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, community_pk):
        community = get_object_or_404(Community, pk=community_pk)
        data = request.data
        data['community'] = community.pk
        data['author'] = request.user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user, community=community)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, community_pk, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, community__id=community_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def patch(self, request, community_pk, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, community__id=community_pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, community_pk, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, community__id=community_pk)
        comment.delete()
        return Response({"message": "삭제완료"}, status=status.HTTP_204_NO_CONTENT)


class CommentLike(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'comment_id'

    def partial_update(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('comment_id')
        instance = self.get_object()
        user = request.user

        if instance.is_liked_by_user(user):
            instance.unlike(user)
            liked = False
        else:
            instance.like(user)
            liked = True

        instance.save()

        likes_count = instance.get_likes_count()

        return Response({'liked': liked, 'likes_count': likes_count}, status=status.HTTP_200_OK)


class CommentsList(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentsListPagination

    def get_queryset(self):
        community = get_object_or_404(Community, pk=self.kwargs['community_pk'])
        return Comment.objects.filter(community=community).order_by('created_at')


class UserCommentsList(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        comments = Comment.objects.filter(
            author=user).order_by('created_at').values()
        replies = Comment.objects.filter(
            author=user, parent_comment__isnull=False).order_by('created_at').values()
        post_list = list(comments) + list(replies)
        post_list.sort(key=lambda x: x['created_at'], reverse=True)
        return Response(post_list)


class ReplyCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        data = request.data
        data['community_comment'] = comment.pk
        data['author'] = request.user.id
        serializer = ReplySerializer(data=data)
        if serializer.is_valid():
            serializer.save(community_comment=comment, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyDetail(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, comment_id, reply_id):
        reply = get_object_or_404(
            Reply, id=reply_id, community_comment__id=comment_id, author=request.user)
        serializer = ReplySerializer(reply, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id, reply_id):
        reply = get_object_or_404(
            Reply, id=reply_id, community_comment__id=comment_id, author=request.user)
        reply.delete()
        return Response({"message": "삭제완료"}, status=status.HTTP_204_NO_CONTENT)


class ReplyLike(generics.UpdateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'reply_id'

    def partial_update(self, request, *args, **kwargs):
        reply_id = self.kwargs.get('reply_id')
        instance = self.get_object()
        user = request.user

        if instance.is_liked_by_user(user):
            instance.unlike(user)
            liked = False
        else:
            instance.like(user)
            liked = True

        instance.save()

        likes_count = instance.get_likes_count()

        return Response({'liked': liked, 'likes_count': likes_count}, status=status.HTTP_200_OK)


class ReplyList(APIView):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        replies = comment.reply_comments.all()
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)


class CommunitySearch(ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommunityFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        search_type = self.request.query_params.get('search_type', None)

        if search_query and search_type:
            if search_type == 'title':
                queryset = queryset.filter(title__icontains=search_query)
            elif search_type == 'content':
                queryset = queryset.filter(content__icontains=search_query)
            elif search_type == 'title_content':
                queryset = queryset.filter(
                    Q(title__icontains=search_query) | Q(content__icontains=search_query))
            elif search_type == 'author':
                queryset = queryset.filter(
                    author__username__icontains=search_query)

        return queryset


class CategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        categories = [{'key': choice[0], 'value': choice[1]} for choice in Community.CATEGORY_CHOICES]
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
