from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    karma = models.IntegerField(default=1)
    nickname = models.CharField(max_length=30, unique=True, null=False, blank=False)  # nickname 필드 수정

    def __str__(self):
        return self.username
