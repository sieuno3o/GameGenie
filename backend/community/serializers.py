from rest_framework import serializers
from .models import Community, Comment, Reply
from accounts.models import User


class CommunitySerializer(serializers.ModelSerializer):
    community_likes = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    community_upvotes = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Community
        fields = ['id', 'type', 'category', 'title', 'content',
                  'link', 'community_likes', 'community_upvotes', 'author', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    comments_likes = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    comments_upvotes = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'community', 'comments', 'author', 'replies',
                  'comments_likes', 'comments_upvotes', 'created_at']

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment_id=obj.id)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data

class ReplySerializer(serializers.ModelSerializer):
    reply_likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    reply_upvotes = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Reply
        fields = ['id', 'community_comment', 'content', 'author',
                  'reply_likes', 'reply_upvotes', 'created_at']
