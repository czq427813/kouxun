from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone

class ArticlePost(models.Model):
    title = models.CharField(max_length=100)
    create_date = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=100)
    url_object_id = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-create_date',)

    def __str__(self):
        return self.title