from rest_framework.response import Response
from community.serializers import CommunitySerializer, CommentSerializer, ReplySerializer
from community.models import Community, Comment, Reply
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from accounts.models import User
from rest_framework import generics


class CommunityList(APIView):
    def get(self, request):
        communities = Community.objects.all()
        for community in communities:
            community.points = community.community_points()
        sorted_communities = sorted(
            communities, key=lambda x: x.points, reverse=True)
        serializer = CommunitySerializer(sorted_communities, many=True)
        return Response(serializer.data)


class CommunityCreate(APIView):
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
        replies = Reply.objects.filter(
            community_comment__community=community).order_by('created_at').values()
        community_list = list(comments) + list(replies)
        community_list.sort(key=lambda x: x['created_at'], reverse=True)
        return Response(community_list)


class UserCommentsListView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        comments = Comment.objects.filter(
            author=user).order_by('created_at').values()
        replies = Reply.objects.filter(
            author=user).order_by('created_at').values()
        post_list = list(comments) + list(replies)
        post_list.sort(key=lambda x: x['created_at'], reverse=True)
        return Response(post_list)


class ReplyCreateAPIView(APIView):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = ReplySerializer(data=request.data)
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
