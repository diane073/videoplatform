from django.db import models
from django.conf import settings

class Feed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=100)
    context = models.TextField(blank=True)
    image = models.ImageField(blank=True,upload_to="/photo/%Y/%m/%d")
    video = models.FileField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes_feed")
    def __str__(self):
        return self.title