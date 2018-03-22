from django.db import models

class Post(models.Model):
    author = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img_path = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.title