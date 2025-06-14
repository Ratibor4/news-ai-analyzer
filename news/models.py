from datetime import datetime

from django.db import models
from django.utils.timezone import make_aware


class News(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField()
    content = models.TextField()
    summary = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    sentiment = models.CharField(max_length=20, blank=True)
    published_at=make_aware(datetime.now()),

    published_at = models.DateTimeField()

    def __str__(self):
        return self.title

