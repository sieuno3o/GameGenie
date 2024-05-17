from rest_framework.response import Response
from .filters import CommunityFilter 
from community.serializers import CommunitySerializer, CommentSerializer, ReplySerializer
from community.models import Community, Comment, Reply
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from accounts.models import User
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q



class CommunityList(APIView):
    def get(self, request):
        communities = Community.objects.all()
        for community in communities:
            community.points = community.communitylist_points()
        sorted_communities = sorted(
            communities, key=lambda x: x.points, reverse=True)
        serializer = CommunitySerializer(sorted_communities, many=True)
        return Response(serializer.data)

class CommunityCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['author'] = request.user.id
        serializer = CommunitySerializer(data=data)
        if serializer.is_valid():
            community = serializer.save(author=request.user)
            return Response({"message": "등록완료", "communityId": community.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommunityDetail(APIView):
    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = CommunitySerializer(community)
        return Response(serializer.data)

    def patch(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = CommunitySerializer(
            community, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "수정완료"}, serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        community.delete()
        return Response({"message": "삭제완료"}, status=status.HTTP_204_NO_CONTENT)

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

class CommentUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, community_id, comment_id):
        comment = get_object_or_404(
            Comment, pk=comment_id, community__id=community_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def patch(self, request, community_id, comment_id):
        comment = get_object_or_404(
            Comment, pk=comment_id, community__id=community_id)
        serializer = CommentSerializer(
            comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, community_id, comment_id):
        comment = get_object_or_404(
            Comment, pk=comment_id, community__id=community_id)
        comment.delete()
        return Response({"message": "삭제완료"}, status=status.HTTP_204_NO_CONTENT)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentsList(APIView):
    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        comments = Comment.objects.filter(
            community=community).order_by('created_at').values()
        replies = Comment.objects.filter(
            parent_comment__community=community).order_by('created_at').values()
        community_list = list(comments) + list(replies)
        community_list.sort(key=lambda x: x['created_at'], reverse=True)
        return Response(community_list)

class UserCommentsListView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        comments = Comment.objects.filter(
            author=user).order_by('created_at').values()
        replies = Comment.objects.filter(
            author=user, parent_comment__isnull=False).order_by('created_at').values()
        post_list = list(comments) + list(replies)
        post_list.sort(key=lambda x: x['created_at'], reverse=True)
        return Response(post_list)

class ReplyCreateAPIView(APIView):
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

class ReplyListAPIView(APIView):
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
                queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
            elif search_type == 'author':
                queryset = queryset.filter(author__username__icontains=search_query)
        
        return queryset