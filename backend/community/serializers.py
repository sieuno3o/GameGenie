from rest_framework import serializers
from .models import Community, Comment, Reply
from accounts.models import User


class CommunitySerializer(serializers.ModelSerializer):
    community_likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    communitylist_points = serializers.IntegerField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)  # 조회수 필드 추가

    class Meta:
        model = Community
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    comments_likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    author_profile_image = serializers.ImageField(source='author.profile_image', read_only=True)  # 프로필 이미지 추가
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment_id=obj.id)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data


class ReplySerializer(serializers.ModelSerializer):
    reply_likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)

    class Meta:
        model = Reply
        fields = '__all__'


class CategorySerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()
