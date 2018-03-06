from django.db import models

# Create your models here.
class Sroom1(models.Model):
    reserved = models.DateTimeField()
    sid = models.TextField()
