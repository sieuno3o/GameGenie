from django.db import models
from django.conf import settings


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=255)
    game_image = models.URLField()
    game_review = models.TextField()
    game_price = models.CharField(max_length=50)
    game_url = models.URLField()

    class Meta:
        unique_together = ('user', 'game_name')

    def __str__(self):
        return f'{self.user.username} - {self.game_name}'
