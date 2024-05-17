from django.db import models
from accounts.models import User
from django.utils import timezone


class Community(models.Model):
    TYPE_CHOICES = [('news', 'News'), ('show', 'Show'), ('ask', 'Ask')]
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField()
    community_like = models.ManyToManyField(
        User, related_name='liked_communities', blank=True)
    community_upvote = models.ManyToManyField(
        User, related_name='upvoted_communities', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def communitylist_points(self):
        after_day = (timezone.now() - self.created_at).days
        after_day_point = -5 * after_day

        comments_count = self.comments.count()
        comments_count_point = 3 * comments_count

        likes_count = self.community_like.count()
        likes_count_point = 1 * likes_count

        return after_day_point + comments_count_point + likes_count_point


class Comment(models.Model):
    community = models.ForeignKey(
        Community, related_name='comments', on_delete=models.CASCADE)
    comments = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comments_likes = models.ManyToManyField(
        User, related_name='liked_comments', blank=True)
    comments_upvotes = models.ManyToManyField(
        User, related_name='upvoted_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_together = ['community', 'author']
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


class Reply(models.Model):
    community_comment = models.ForeignKey(
        Comment, related_name='reply_comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_likes = models.ManyToManyField(
        User, related_name='liked_replies', blank=True)
    reply_upvotes = models.ManyToManyField(
        User, related_name='upvoted_replies', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
