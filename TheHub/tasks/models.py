from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization

class Task(models.Model):
    title = models.CharField(max_length = 100)
    description= models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey( Organization , on_delete=models.CASCADE)