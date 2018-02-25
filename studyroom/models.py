from django.db import models

# Create your models here.
class Sroom1(models.Model):
    reserved = models.DateTimeField()
    name1 = models.TextField()
    sid1 = models.TextField()
    name2 = models.TextField()
    sid2 = models.TextField()
